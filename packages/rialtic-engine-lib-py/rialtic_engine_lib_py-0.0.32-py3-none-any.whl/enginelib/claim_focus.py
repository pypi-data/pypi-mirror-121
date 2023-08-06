import datetime as dt
import re
from enum import Enum
from typing import Dict, List, Optional, Union, cast, Set

from fhir.resources.address import Address
from fhir.resources.claim import Claim, ClaimInsurance, ClaimItem, ClaimRelated, ClaimSupportingInfo
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.coverage import Coverage
from fhir.resources.fhirtypes import Date, Decimal
from fhir.resources.identifier import Identifier
from fhir.resources.money import Money
from fhir.resources.organization import Organization
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.practitionerrole import PractitionerRole
from fhir.resources.reference import Reference
from fhir.resources.resource import Resource
from fhir.resources.servicerequest import ServiceRequest
from schema.insight_engine_request import InsightEngineRequest

from enginelib.claim_insurance_focus import (ClaimInsuranceFocus,
                                             find_primary_insurance)
from enginelib.claim_line_focus import ClaimLineFocus
from enginelib.comparator import ClaimComparator, CompareResult
from enginelib.errors import ClaimError
from enginelib.types import Period


class ClaimTypeFocus(str, Enum):
    PROFESSIONAL = "professional"
    INSTITUTIONAL = "institutional"
    DENTAL = "dental"
    PHARMACY = "pharmacy"

    @staticmethod
    def get_claim_type_set():
        return (
            (
                {"cms1500", "837p", "005010x222", "professional", "vision"},
                ClaimTypeFocus.PROFESSIONAL
            ),
            (
                {"ub04", "837i", "005010x223", "institutional"},
                ClaimTypeFocus.INSTITUTIONAL
            ),
            (
                {"ada2006", "837d", "005010x224", "dental", "oral"},
                ClaimTypeFocus.DENTAL
            ),
            (
                {"837", "ncpdpd0", "ncpdpbatch12",
                 "ncpdpwcpcucf", "pharmacy", "drug"},
                ClaimTypeFocus.PHARMACY
            )
        )

    @classmethod
    def from_string(cls, value: str) -> "ClaimTypeFocus":
        normalized_value = re.sub("[^0-9a-z]", "", value.lower())

        for values, claim_type in cls.get_claim_type_set():
            if normalized_value in values:
                return cls.__new__(cls, claim_type)

        raise ClaimError("Unsupported claim type %s" % value)


class ClaimFocus:
    _fields_looked_at: Set[str] = set()

    def __init__(self, claim: Claim, request: InsightEngineRequest = None):
        self.claim = claim
        self.request = request if request is not None else InsightEngineRequest(
            claim=claim)
        self._contained: Optional[Dict[str, Resource]] = None
        self._lines: Optional[List[ClaimLineFocus]] = None

    @property
    def contained(self) -> Dict[str, Resource]:
        self._fields_looked_at.add('contained')
        if self._contained is not None:
            return self._contained

        self._contained = dict()
        if getattr(self.claim, "contained", None):
            resources = [cast(Resource, elem) for elem in self.claim.contained]
            self._contained = {
                resource.id: resource for resource in resources
                if resource.id is not None
            }

        return self._contained

    @property
    def lines(self) -> Optional[List[ClaimLineFocus]]:
        self._fields_looked_at.add('lines')
        if self._lines is not None:
            return self._lines

        if self.request is None:
            self.request = InsightEngineRequest.construct(claim=self.claim)

        self._lines = [ClaimLineFocus(cast(ClaimItem, c), self.request)
                       for c in self.claim.item]
        return self._lines

    def _get_organization(self):
        org = self.provider
        if not isinstance(org, Organization):
            raise ClaimError(f"Organization not found on claim.")
        return org

    @property
    def svc_facility_name(self) -> str:
        self._fields_looked_at.add('svc_facility_name')
        org = self._get_organization()
        try:
            if org.name:
                return org.name
            raise AttributeError()
        except AttributeError:
            raise ClaimError(f"Field svcFacilityName not found on claim.")

    def _svc_facility_add(self, index: int) -> str:
        """
        Args:
            index: 0 for svcFacilityAdd1 or 1 for svcFacilityAdd2
        """
        org = self._get_organization()
        try:
            address = cast(Address, org.address[0])
            line = address.line[index]
            if line:
                return line
            raise AttributeError()
        except (AttributeError, IndexError):
            raise ClaimError(f"Field svcFacilityAdd{index + 1} not found on claim.")

    @property
    def svc_facility_add1(self) -> str:
        self._fields_looked_at.add('svc_facility_add1')
        return self._svc_facility_add(0)

    @property
    def svc_facility_add2(self) -> str:
        self._fields_looked_at.add('svc_facility_add2')
        return self._svc_facility_add(1)

    @property
    def svc_facility_city(self) -> str:
        self._fields_looked_at.add('svc_facility_city')
        org = self._get_organization()
        try:
            city = cast(Address, org.address[0]).city
            if city:
                return city
            raise AttributeError()
        except AttributeError:
            raise ClaimError(f"Field svcFacilityCity not found on claim.")

    @property
    def svc_facility_state(self) -> str:
        self._fields_looked_at.add('svc_facility_state')
        org = self._get_organization()
        try:
            state = cast(Address, org.address[0]).state
            if state:
                return state
            raise AttributeError()
        except AttributeError:
            raise ClaimError(f"Field svcFacilityState not found on claim.")

    @property
    def svc_facility_zip(self) -> str:
        self._fields_looked_at.add('svc_facility_add1')
        org = self._get_organization()
        try:
            postal_code = cast(Address, org.address[0]).postalCode
            if postal_code:
                return postal_code
            raise AttributeError()
        except AttributeError:
            raise ClaimError(f"Field svcFacilityZip not found on claim.")

    @property
    def patient(self) -> Patient:
        self._fields_looked_at.add('patient')
        try:
            ref = cast(Reference, self.claim.patient).reference
        except AttributeError:
            raise ClaimError(f"reference to patient not found on claim")
        try:
            return self.contained[ref]
        except KeyError:
            raise ClaimError(
                f"Patient with id: {ref} not found in contained objects")

    @property
    def patient_birthDate(self) -> dt.date:
        self._fields_looked_at.add('patient_birthDate')
        """
        Birth Date of patient
        """
        try:
            patient = self.patient
        except (ClaimError):
            raise ClaimError("Paitent not found on claim")

        try:
            birthDate = patient.birthDate
            return birthDate
        except AttributeError:
            raise ClaimError(
                f"Birthdate not found on patient with id {self.patient.id}")

    @property
    def provider(self) -> Union[Practitioner, Organization, PractitionerRole]:
        self._fields_looked_at.add('provider')
        try:
            ref = cast(Reference, self.claim.provider).reference
        except AttributeError:
            raise ClaimError("reference to provider not found on the claim")
        try:
            return self.contained[ref]
        except KeyError:
            raise ClaimError(
                f"provider with id: {ref} not found in contained objects")

    @property
    def date_current_illness(self) -> dt.date:
        self._fields_looked_at.add('date_current_illness')
        try:
            supporting_info = cast(List[ClaimSupportingInfo], self.claim.supportingInfo)
            for info in supporting_info:
                try:
                    coding = cast(CodeableConcept, info.category).coding
                    code = cast(Coding, coding[0]).code
                    if code != 'onset':
                        continue
                    period = cast(Period, info.timingPeriod)
                    if period.start:
                        return period.start
                except AttributeError:
                    pass
            raise AttributeError()
        except (AttributeError, KeyError, TypeError):
            raise ClaimError('Field dateCurrentIllness not found on claim.')

    @property
    def attachments(self) -> List[str]:
        self._fields_looked_at.add('attachments')
        try:
            target = list()
            info_list = cast(List[ClaimSupportingInfo], self.claim.supportingInfo)
            for info in info_list:
                category = cast(CodeableConcept, info.category)
                code = cast(Coding, category.coding[0]).code
                if code == 'attachment':
                    target.append(info.valueString)
            if target:
                return target
            raise AttributeError()
        except (AttributeError, IndexError, TypeError):
            return list()

    @property
    def claim_type(self) -> str:
        self._fields_looked_at.add('claim_type')
        try:
            code = cast(Coding,
                        cast(CodeableConcept,
                             self.claim.type
                             ).coding[0]
                        ).code
            if not code:
                raise ClaimError()
            return code
        except (AttributeError, IndexError, ClaimError):
            raise ClaimError("No type found on this claim")

    @property
    # TODO(plyq): replace existing `claim_type` with this once versioning will be done.
    def claim_type_normalized(self) -> ClaimTypeFocus:
        self._fields_looked_at.add('claim_type_normalized')
        return ClaimTypeFocus.from_string(self.claim_type)

    @property
    def relatedClaimRelations(self) -> List[str]:
        self._fields_looked_at.add('relatedClaimRelations')
        if self.claim.related is None:
            return []

        try:
            codes = []
            for rel in self.claim.related:
                code = cast(
                    Coding,
                    cast(
                        CodeableConcept,
                        cast(
                            ClaimRelated,
                            rel
                        ).relationship
                    ).coding[0]
                ).code
                codes.append(code)
            return codes
        except (AttributeError, TypeError):
            raise ClaimError("")

    @property
    def pre_auth_ref(self) -> List[str]:
        self._fields_looked_at.add('pre_auth_ref')
        try:
            insurance = cast(List[ClaimInsurance], self.claim.insurance)
            for ins in insurance:
                if ins.sequence == 1:
                    if ins.preAuthRef:
                        return ins.preAuthRef
            raise AttributeError()
        except (AttributeError, TypeError):
            raise ClaimError('Field preAuthRef not found on claim.')

    @staticmethod
    def _cleanup(ref: str) -> str:
        return ref[1:] if ref and ref[0] == '#' else ref

    @property
    def referring_provider(self) -> Optional[Union[Practitioner, Organization]]:
        self._fields_looked_at.add('referring_provider')
        try:
            ref = cast(Reference, self.claim.referral).reference
            ref = self._cleanup(ref)
            service_request = cast(ServiceRequest, self.contained[ref])
            ref = cast(Reference, service_request.requester).reference
            provider = self.contained[ref]
            if provider:
                if provider.resource_type.lower() == 'practitioner':
                    return cast(Practitioner, provider)
                if provider.resource_type.lower() == 'organization':
                    return cast(Organization, provider)
                raise AttributeError()
        except (AttributeError, KeyError, TypeError):
            raise ClaimError(f"Referring provider not found on this claim.")

    @property
    def ordering_provider(self) -> Optional[Union[Practitioner, Organization]]:
        """In the OLD FHIR mapping, there are three sets of fields that are mapped to the same
        place providerReferring*, providerOrdering* and providerSupervising*
        This is why we just make an alias to referring_provider here."""
        self._fields_looked_at.add('ordering_provider')
        return self.referring_provider

    @property
    def supervising_provider(self) -> Optional[Union[Practitioner, Organization]]:
        """In the OLD FHIR mapping, there are three sets of fields that are mapped to the same
        place providerReferring*, providerOrdering* and providerSupervising*
        This is why we just make an alias to referring_provider here."""
        self._fields_looked_at.add('supervising_provider')
        return self.referring_provider

    # noinspection DuplicatedCode
    @staticmethod
    def practitioner_identifiers(provider: Union[Practitioner, Organization]) -> Dict[str, str]:
        ids = dict()
        for prov_id in provider.identifier:
            if hasattr(prov_id, 'type') and prov_id.type:
                prov_id_type = cast(
                    Coding,
                    cast(
                        CodeableConcept,
                        prov_id.type
                    ).coding[0]
                ).code.upper()
            else:
                # The default type is assumed to be NPI
                prov_id_type = 'NPI'

            # ATTENTION: assuming each Practitioner referenced in a claim line
            #     has only one identifier of each type.
            ids[prov_id_type] = cast(
                Identifier,
                prov_id
            ).value.strip()

        return ids

    @property
    def referring_npi_number(self) -> str:
        self._fields_looked_at.add('referring_npi_number')
        referring_provider = self.referring_provider
        try:
            identifiers = self.practitioner_identifiers(referring_provider)
            return identifiers['NPI']
        except (KeyError, ClaimError):
            raise ClaimError('Field orderingNPINumber not found on this claim.')

    @property
    def ordering_npi_number(self) -> str:
        self._fields_looked_at.add('ordering_npi_number')
        return self.referring_npi_number

    @property
    def supervising_npi_number(self) -> str:
        self._fields_looked_at.add('supervising_npi_number')
        return self.referring_npi_number

    @property
    def subscriberIDs(self) -> List[str]:
        # |claim.insurance| = 1..*.
        self._fields_looked_at.add('subscriberIDs')
        if not self.claim.insurance:
            raise ClaimError("No insurance found on this claim")

        ids = []
        for ins in self.claim.insurance:
            claim_ins = cast(ClaimInsurance, ins).coverage
            try:
                ref = cast(Reference, claim_ins).reference
                cov = self.contained[ref]
            except KeyError:
                continue

            sub_id = cast(Coverage, cov).subscriberId
            if sub_id is not None:
                ids.append(sub_id)
        return ids

    @property
    def totalChargedAmount(self) -> Optional[Decimal]:
        self._fields_looked_at.add('totalChargedAmount')
        if self.claim.total:
            if cast(Money, self.claim.total).value is not None:
                return cast(Money, self.claim.total).value
        return None

    @property
    def bill_type(self) -> str:
        self._fields_looked_at.add('bill_type')
        # Claim.subType.coding.code
        try:
            code = cast(Coding,
                        cast(CodeableConcept,
                             self.claim.subType
                             ).coding[0]
                        ).code
            if not code:
                raise ClaimError()
            return code
        except (AttributeError, IndexError, ClaimError):
            raise ClaimError("No bill type found on this claim")

    @property
    def claim_num(self) -> str:
        self._fields_looked_at.add('claim_num')
        try:
            return self.claim.identifier[0].value
        except (IndexError, AttributeError, TypeError) as exc:
            raise ClaimError("Could not find claimNum") from exc

    @property
    def hospitalized_period(self) -> Period:
        """
        Hospitalization Period for claim.

        NOTE: It is different with claim line hospitalization properties.

        Returns
        -------
            If the claim has a single hospitalizatoin timing date, both
            dates in this tuple will be same. Otherwise they will be start
            and end date of hospitalization timing period
        """
        self._fields_looked_at.add('hospitalized_period')
        try:
            # Found supportingInfo related to hospitalization.
            infos = self.claim.supportingInfo
            found_info = None
            for info in infos:
                category = cast(
                    Coding,
                    cast(
                        CodeableConcept,
                        info.category
                    ).coding[0]
                ).code
                if category == "hospitalized":
                    if found_info:
                        raise ClaimError
                    else:
                        found_info = info
            # No hospitalized.
            if not found_info:
                raise ClaimError
            # Found timing period for that info.
            timing_date = found_info.timingDate
            if timing_date:
                return Period(timing_date, timing_date)
            else:
                period = found_info.timingPeriod
                if not (period.start and period.end):
                    raise ClaimError()
                return Period(period.start, period.end)
        except (AttributeError, ClaimError, TypeError):
            raise ClaimError(
                "Hospitalized period not found for this claim"
            )

    @property
    def admit_date(self) -> Date:
        self._fields_looked_at.add('admit_date')
        try:
            return self.hospitalized_period[0]
        except ClaimError as exc:
            raise ClaimError("Admit date not found for this claim") from exc

    def __eq__(self, other: object) -> bool:
        """Check that claim id-s are same.

        Args:
            other: claim focus to compare

        Returns:
            True if id-s are the same

        Raises:
            NotImplementedError: if comparing with non-ClaimFocus
            ClaimError: if there are not any id.
        """
        if not isinstance(other, ClaimFocus):
            raise NotImplementedError(
                "ClaimFocus object is comparable only "
                "with another ClaimFocus object"
            )
        compare_result = ClaimComparator.compare(self.claim, other.claim)
        return compare_result == CompareResult.EQ

    @property
    def insurance(self) -> List[ClaimInsurance]:
        self._fields_looked_at.add('insurance')
        try:
            return [
                cast(ClaimInsurance, insurance)
                for insurance in self.claim.insurance
            ]
        except AttributeError:
            raise ClaimError(f"Insurance not found on claim")

    @property
    def primary_insurance(self) -> ClaimInsurance:
        self._fields_looked_at.add('primary_insurance')
        return find_primary_insurance(self.insurance, self.request)

    @property
    def subscriber_id(self) -> str:
        """Subscriber id for the primary coverage.

        1. If subscriberId is present, return it
        2. If there is only one identifier, return it
        3. Go thru all identifiers and find the one from each all others start
        4. If such identifier doesn't exist, raise ClaimError
        """
        self._fields_looked_at.add('subscriber_id')
        primary_insurance = ClaimInsuranceFocus(
            self.primary_insurance, request=self.request)
        return primary_insurance.subscriber_id

    @property
    def relation_to_insured(self) -> str:
        """Relationship from the primary coverage."""
        self._fields_looked_at.add('relation_to_insured')
        primary_insurance = ClaimInsuranceFocus(
            self.primary_insurance, request=self.request)
        return primary_insurance.relation_to_insured

    @property
    def group_num(self) -> str:
        """
        Returns the Value of coverage class type "group"
        primary insurance
        :return: str
        """
        self._fields_looked_at.add('group_num')
        primary_insurance = ClaimInsuranceFocus(
            self.primary_insurance, request=self.request)
        return primary_insurance.group_number

    @property
    def group_name(self) -> str:
        """
        Returns the Name of coverage class type "group"
        primary insurance
        :return: str
        """
        self._fields_looked_at.add('group_name')
        primary_insurance = ClaimInsuranceFocus(
            self.primary_insurance, request=self.request)
        return primary_insurance.group_name

    @classmethod
    def used_fields(cls) -> Set[str]:
        return cls._fields_looked_at
