import datetime as dt
from typing import Dict, List, Optional, Union, cast, Set

from fhir.resources.claim import (ClaimCareTeam, ClaimDiagnosis,
                                  ClaimInsurance, ClaimItem)
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.encounter import Encounter
from fhir.resources.fhirtypes import Date, Decimal, PositiveInt
from fhir.resources.identifier import Identifier
from fhir.resources.organization import Organization
from fhir.resources.patient import Patient
from fhir.resources.period import Period as FHIRPeriod
from fhir.resources.practitioner import Practitioner
from fhir.resources.practitionerrole import PractitionerRole
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from fhir.resources.resource import Resource
from schema.insight_engine_request import InsightEngineRequest

import enginelib.utils as elut
from enginelib.claim_insurance_focus import (ClaimInsuranceFocus,
                                             find_primary_insurance)
from enginelib.comparator import (ClaimComparator, ClaimItemComparator,
                                  CompareResult)
from enginelib.errors import ClaimError
from enginelib.resources import contained_resources
from enginelib.types import Period
import warnings


class ClaimLineFocus:
    """
    A class that provides easy access to attributes on claim lines
    """

    _fields_looked_at: Set[str] = set()

    def __init__(self, claim_line: ClaimItem, request: InsightEngineRequest):
        self.claim_line = claim_line
        self.request = request

        self._contained: Optional[Dict[str, Resource]] = None

    @property
    def contained(self) -> Dict[str, Resource]:
        self._fields_looked_at.add('contained')
        if self._contained is not None:
            return self._contained

        # set up references for contained elements
        self._contained = dict()
        if getattr(self.request.claim, "contained", None):
            resources = [cast(Resource, elem) for elem in self.request.claim.contained]
            self._contained = {
                resource.id: resource for resource in resources
                if resource.id is not None
            }

        return self._contained

    @property
    def procedure_code(self) -> str:
        """
        Procedure Code for claim line

        Returns
        _______

        """
        self._fields_looked_at.add('procedure_code')
        try:
            code = cast(List[Coding],
                        cast(CodeableConcept,
                             self.claim_line.productOrService
                             ).coding
                        )[0].code
            if not code:
                raise ClaimError()
            return code
        except (IndexError, AttributeError, ClaimError):
            raise ClaimError('Procedure code not found for this claim line')
        return code

    @property
    def ndc_code(self) -> List[str]:
        """
        NDC Code for claim line
        Returns
        -------
            ndcCode of Claim Line, if present
        """
        self._fields_looked_at.add('ndc_code')
        try:
            references = cast(Reference, self.claim_line.udi)
            if not references:
                raise ClaimError('NDC Code not found for this claim line')
        except (AttributeError, ClaimError):
            raise ClaimError('NDC Code not found for this claim line')

        try:
            devices = [self.contained[reference.reference] for reference in references]
        except KeyError as e:
            raise ClaimError(f"Device with id: {e.args[0]} not found in contained objects")

        ndc_codes = list()
        for device in devices:
            ndc_codes.extend([identifier.value for identifier in device.identifier if identifier.system == "NDC"])

        if not ndc_codes:
            raise ClaimError("No Device with Identifier type NDC found in this claim line")
        return ndc_codes

    @property
    def service_period(self) -> Period:
        """
        Service Period for claim line

        Returns
        -------
            If the claim line has a single service date, both dates in this tuple will be same
            Otherwise they will be start and end date of service period
        """
        self._fields_looked_at.add('service_period')
        try:
            serv_date = self.claim_line.servicedDate
            if serv_date:
                return Period(serv_date, serv_date)
            else:
                period = cast(FHIRPeriod, self.claim_line.servicedPeriod)
                if not (period.start and period.end):
                    raise ClaimError()
                return Period(period.start, period.end)
        except (AttributeError, ClaimError):
            raise ClaimError('Service period not found for this claim line')

    @property
    def patient(self) -> Patient:
        self._fields_looked_at.add('patient')
        try:
            ref = cast(Reference, self.request.claim.patient).reference
        except AttributeError:
            raise ClaimError(f"Patient not found on claim")
        try:
            return self.contained[ref]
        except KeyError:
            raise ClaimError(f"Patient with id: {ref} not found in contained objects")

    @property
    def provider(self) -> Union[Practitioner, PractitionerRole, Organization]:
        self._fields_looked_at.add('provider')
        try:
            ref = cast(Reference, self.request.claim.provider).reference
        except AttributeError:
            raise ClaimError(f"Provider not found on claim")
        try:
            return self.contained[ref]
        except KeyError:
            raise ClaimError(f"Provider with id: {ref} not found in contained objects")

    # TODO(*): Remove old `provider`, rename this to `provider`.
    @property
    def provider_future(self) -> Practitioner:
        """Provider property from specifications."""
        self._fields_looked_at.add('provider_future')
        provider = None
        claim_line = self.claim_line
        claim = self.request.claim
        claim_resources = contained_resources(claim)

        # Create {sequence: careTeam} dict to easy find items.
        care_teams = {
            cast(ClaimCareTeam, care_team).sequence: care_team
            for care_team in claim.careTeam
        }
        for index in claim_line.careTeamSequence:
            try:
                provider_id = cast(
                    Reference,
                    cast(
                        ClaimCareTeam,
                        care_teams[index]  # might raise KeyError
                    ).provider
                ).reference
            except KeyError:
                # Provider indexed in field claim_line.careTeamSequence
                #     was not present in claim.careTeam:
                continue

            if provider_id not in claim_resources:
                continue

            resource = claim_resources[provider_id]
            if resource.resource_type != 'Practitioner':
                continue

            if provider is not None:
                # NOTE: checked with analysts: it is ok to assume only
                #     one practitioner per claim line.
                raise ClaimError("Too many practitioners")

            provider = cast(Practitioner, resource)

        if provider is None:
            raise ClaimError("No practitioner")

        return provider

    @property
    def practitioner(self) -> Practitioner:
        """
        note: this property exists for backwards compatibility
        """
        self._fields_looked_at.add('practitioner')
        return self.provider

    @property
    def patient_age(self) -> int:
        """
        Age of patient on service date or start of service period

        Notes
        -----
        Patient age may differ from one line to the next if the
        beginning of service differs
        """
        self._fields_looked_at.add('patient_age')
        try:
            birth = self.patient.birthDate
            start, _ = self.service_period
            return elut.date_diff(start, birth, unit="year")
        except AttributeError:
            raise ClaimError(f"Birthdate not found on patient with id {self.patient.id}")

    @property
    def modifier_codes(self) -> List[str]:
        self._fields_looked_at.add('modifier_codes')
        try:
            codes = [
                coding.code
                for codings in [
                    cast(List[Coding], c.coding)
                    for c in cast(List[CodeableConcept], self.claim_line.modifier)
                ]
                for coding in codings
            ]
            return codes
        except (AttributeError, TypeError):
            raise ClaimError("Modifiers not found on this claim line")

    @property
    def location_codes(self) -> List[str]:
        self._fields_looked_at.add('location_codes')
        try:
            return [
                cast(Coding, c).code
                for c in cast(
                    CodeableConcept,
                    self.claim_line.locationCodeableConcept
                ).coding
            ]
        except (AttributeError, TypeError):
            raise ClaimError("No location codes found for this claim line")

    @property
    def claim_type(self) -> str:
        self._fields_looked_at.add('claim_type')
        try:
            code = cast(Coding,
                        cast(CodeableConcept,
                             self.request.claim.type
                             ).coding[0]  # why is this a list? what are the other items? can claim have multiple types?
                        ).code
            if not code:
                raise ClaimError()
            return code
        except (AttributeError, IndexError, ClaimError):
            raise ClaimError("No type found on this claim")

    @property
    def pos_code(self) -> str:
        """
        `DEPRECATED`
        Same as `place_of_service` property

        Returns:
            placeOfService property if exists

        Raises:
            ClaimError: if placeOfService extraction failed
        """
        self._fields_looked_at.add('pos_code')
        return self.place_of_service

    # TODO(plyq): Part of ClaimFocus. Remove after versioning.
    @property
    def insurance(self) -> List[ClaimInsurance]:
        self._fields_looked_at.add('insurance')
        try:
            return [
                cast(ClaimInsurance, insurance)
                for insurance in self.request.claim.insurance
            ]
        except AttributeError:
            raise ClaimError(f"Insurance not found on claim")

    # TODO(plyq): Part of ClaimFocus. Remove after versioning.
    @property
    def primary_insurance(self) -> ClaimInsurance:
        self._fields_looked_at.add('primary_insurance')
        return find_primary_insurance(self.insurance, self.request)

    # TODO(plyq): Part of ClaimFocus. Remove after versioning.
    @property
    def subscriber_id(self) -> str:
        """Subscriber id for the primary coverage.

        1. If subscriberId is present, return it
        2. If there is only one identifier, return it
        3. Go thru all identifiers and find the one from each all others start
        4. If such identifier doesn't exist, raise ClaimError
        """
        self._fields_looked_at.add('subscriber_id')
        primary_insurance = ClaimInsuranceFocus(self.primary_insurance, request=self.request)
        return primary_insurance.subscriber_id

    @property
    def diagnosis_codes(self) -> List[str]:
        self._fields_looked_at.add('diagnosis_codes')
        try:
            return [
                coding.code
                for codings in [
                    cast(List[Coding], c.coding)
                    for c in cast(List[CodeableConcept],
                                  [cast(ClaimDiagnosis, concept).diagnosisCodeableConcept for concept in
                                   self.request.claim.diagnosis])]
                for coding in codings
            ]
        except (AttributeError, TypeError, ClaimError):
            raise ClaimError("No Diagnosis codes found for this claim line.")

    @property
    def primary_diagnosis_pointer_code(self) -> str:
        self._fields_looked_at.add('primary_diagnosis_pointer_code')
        try:
            try:
                diagPointer = self.claim_line.diagnosisSequence[0]
            except (IndexError):
                raise ClaimError("No Diagnosis pointer found for this claim line.")
            return cast(List[Coding],
                        cast(ClaimDiagnosis, self.request.claim.diagnosis[diagPointer-1])
                        .diagnosisCodeableConcept).coding[0].code
        except (AttributeError, TypeError, ClaimError):
            raise ClaimError("No Diagnosis codes found for this diagnosis sequence.")

    @property
    def diag_pointers(self) -> List[str]:
        self._fields_looked_at.add('diag_pointers')
        if not hasattr(self.claim_line, 'diagnosisSequence') or \
                not isinstance(self.claim_line.diagnosisSequence, list):
            return list()

        diagnoses = list()
        for i, index in enumerate(self.claim_line.diagnosisSequence):
            try:
                claim_diagnosis = cast(ClaimDiagnosis, self.request.claim.diagnosis[index - 1])
                diagnosis_codeable_concept = cast(CodeableConcept, claim_diagnosis.diagnosisCodeableConcept)
                diagnosis = cast(Coding, diagnosis_codeable_concept.coding[0]).code
                diagnoses.append(diagnosis)
            except (AttributeError, TypeError, IndexError):
                raise ClaimError(f'Field diagPointer{i} could not be determined for this claim line.')

        return diagnoses

    @property
    def program_indicators(self) -> List[str]:
        self._fields_looked_at.add('program_indicators')
        try:
            indicators: Set[str] = set()
            for codeable_concept in cast(List[CodeableConcept], self.claim_line.programCode):
                for coding in cast(List[Coding], codeable_concept.coding):
                    indicators.add(coding.code)
            if indicators:
                return list(indicators)
            raise AttributeError()
        except (AttributeError, TypeError):
            raise ClaimError('Field programIndicator not found in this claim line.')

    @property
    def quantity(self) -> Decimal:
        self._fields_looked_at.add('quantity')
        try:
            return cast(Quantity, self.claim_line.quantity).value
        except (AttributeError, ClaimError):
            raise ClaimError("No quantity value found fo this claim.")

    @property
    def sequence(self) -> PositiveInt:
        self._fields_looked_at.add('sequence')
        try:
            return self.claim_line.sequence
        except (AttributeError, ClaimError):
            raise ClaimError("No sequence value found for this claim.")

    @property
    def other_claim_line(self) -> List[ClaimItem]:
        """
        Get OCL on the same claim
        """
        self._fields_looked_at.add('other_claim_line')
        warnings.warn("other_claim_line is deprecated. "
                      "Please use other_claim_lines instead that returns ClaimLineFocus",
                      DeprecationWarning)
        return [cast(ClaimItem, claim_item) for claim_item in self.request.claim.item if claim_item is not self.claim_line]

    @property
    def other_claim_lines(self) -> List["ClaimLineFocus"]:
        """
        Get OCL on the same claim that are wrapped by ClaimLineFocus
        """
        self._fields_looked_at.add('other_claim_lines')
        return [
            self.__class__(cast(ClaimItem, claim_item), self.request)
            for claim_item in self.request.claim.item
            if claim_item is not self.claim_line
        ]

    @property
    def encounters(self) -> List[Encounter]:
        self._fields_looked_at.add('encounters')
        try:
            refs = [
                cast(Reference, encounter).reference
                for encounter in self.claim_line.encounter
            ]
        except (AttributeError, TypeError):
            raise ClaimError(f"Encounter not found on claim")
        return [
            cast(Encounter, self.contained[ref])
            for ref in refs
            if ref in self.contained
        ]

    @property
    def admit_date(self) -> Date:
        self._fields_looked_at.add('admit_date')
        date_candidates = []
        for encounter in self.encounters:
            try:
                date_ = encounter.period.start
                if encounter.hospitalization.admitSource:
                    date_candidates.append(date_)
            except AttributeError:
                continue
        date_candidates = list(set(date_candidates))
        if len(date_candidates) == 0:
            raise ClaimError("AdmitDate is not found")
        elif len(date_candidates) > 1:
            raise ClaimError("There are at least 2 candidates for admitDate")
        else:
            return date_candidates[0]

    @property
    def discharge_date(self) -> Date:
        self._fields_looked_at.add('discharge_date')
        date_candidates = []
        for encounter in self.encounters:
            try:
                date_ = encounter.period.end
                if encounter.hospitalization.dischargeDisposition:
                    date_candidates.append(date_)
            except AttributeError:
                continue
        date_candidates = list(set(date_candidates))
        if len(date_candidates) == 0:
            raise ClaimError("DischargeDate is not found")
        elif len(date_candidates) > 1:
            raise ClaimError("There are at least 2 candidates for dischargeDate")
        else:
            return date_candidates[0]

    @property
    def revenue_code(self) -> str:
        self._fields_looked_at.add('revenue_code')
        # Claim.item[n].revenue.coding.code
        try:
            code = cast(Coding,
                        cast(CodeableConcept,
                             self.claim_line.revenue
                             ).coding[0]
                        ).code
            if not code:
                raise ClaimError()
            return code
        except (AttributeError, IndexError, ClaimError):
            raise ClaimError("No revenue found on this claim line")

    @property
    def place_of_service(self) -> str:
        """
        Extracts placeOfService for ClaimLime.
        Used `locationCodeableConcept` original field.

        Returns:
            placeOfService property if exists

        Raises:
            ClaimError: if placeOfService extraction failed
        """
        self._fields_looked_at.add('place_of_service')
        try:
            code = cast(List[Coding],
                        cast(CodeableConcept,
                             self.claim_line.locationCodeableConcept
                             ).coding
                        )[0].code
            if not code:
                raise ClaimError()
        except (IndexError, AttributeError, ClaimError):
            raise ClaimError(
                'Place of service code not found for this claim line'
            )
        return code

    @property
    def rend_prov_npi(self) -> str:
        self._fields_looked_at.add('rend_prov_npi')
        return self._find_identifiers("NPI", "NPI number")

    @property
    def rend_prov_taxonomy(self) -> str:
        self._fields_looked_at.add('rend_prov_taxonomy')
        return self._find_identifiers("TAX", "Taxonomy number")

    def other_clf_period_diff(self, other: "ClaimLineFocus", unit: str) -> int:
        """
        :param unit: one of day, month, year
        :return: service period difference in unit-s.
        """
        return elut.date_diff(self.service_period[0], other.service_period[0], unit=unit)

    @staticmethod
    def stub(
            procedure_code: str = "TEST",
            service_start: dt.date = dt.date.min,
            service_end: dt.date = dt.date.max,
            units: int = 0
    ):
        claim_item = ClaimItem.parse_obj({
            "sequence": 1,
            "productOrService": {
                "coding": [
                    {
                        "code": f"{procedure_code}",
                        "system": "http://hl7.org/fhir/ex-serviceproduct"
                    }
                ]
            },
            "quantity": {
                "value": f"{units}"
            },
            #   python datetime library default string format for dates is YYYY-MM-DD
            #   this is the same as HL7 FHIR
            "servicedPeriod": {
                "end": f"{service_end}",
                "start": f"{service_start}"
            }
        })
        return ClaimLineFocus(claim_item, InsightEngineRequest())

    def __eq__(self, other: object) -> bool:
        """Check that claim id-s and claim line sequences are same.

        Args:
            other: claim line focus to compare

        Returns:
            True if id-s and sequences are the same

        Raises:
            NotImplementedError: if comparing with non-ClaimLineFocus
            ClaimError: if there are not any id.
        """
        if not isinstance(other, ClaimLineFocus):
            raise NotImplementedError(
                "ClaimFocus object is comparable only "
                "with another ClaimFocus object"
            )
        compare_results = (
            ClaimComparator.compare(self.request.claim, other.request.claim),
            ClaimItemComparator.compare(self.claim_line, other.claim_line),
        )
        return all(result == CompareResult.EQ for result in compare_results)

    def _find_identifiers(self, id_type: str, id_name: str) -> str:
        id_value: Optional[str] = None
        not_found_error_msg = f"No {id_name} found on this claim line."
        too_many_error_msg = f"Too many {id_name}s in the claim line."

        try:
            identifiers = cast(List[Identifier], self.provider_future.identifier)
            for identifier in identifiers:
                identifier_type = cast(
                    Coding,
                    cast(CodeableConcept, identifier.type).coding[0]
                )
                if identifier_type.code == id_type:
                    if id_value is None:
                        id_value = identifier.value
                    else:
                        # found more than one value of rendProvNPI
                        raise ClaimError(too_many_error_msg)

            if id_value:
                return id_value

            # in case there were identifiers but not of id_type
            raise ClaimError(not_found_error_msg)
        except (ClaimError, AttributeError, TypeError, IndexError):
            # in case there were no identifiers at all
            if id_value is None:
                raise ClaimError(not_found_error_msg)
            else:
                raise ClaimError(too_many_error_msg)


        return id_value

    @classmethod
    def used_fields(cls) -> Set[str]:
        return cls._fields_looked_at

