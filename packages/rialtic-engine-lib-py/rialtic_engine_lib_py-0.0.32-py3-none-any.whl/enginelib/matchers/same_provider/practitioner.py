from typing import Dict, cast, Optional

from fhir.resources.claim import Claim, ClaimItem
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.identifier import Identifier
from fhir.resources.practitioner import Practitioner
from fhir.resources.resource import Resource

from enginelib.claim_focus import ClaimFocus
from enginelib.claim_line_focus import ClaimLineFocus
from enginelib.errors import ClaimError
from enginelib.matchers.same_provider.error import NoPractitionerError, TooManyPractitionersError
from schema.insight_engine_request import InsightEngineRequest


def claim_practitioner(claim: Claim, claim_resources: Dict[str, Resource]) -> Practitioner:
    # Init ClaimFocus.
    claim_with_resources_dict = claim.dict()
    claim_with_resources_dict["contained"] = list(claim_resources.values())
    claim_focus = ClaimFocus(Claim(**claim_with_resources_dict))
    # Retrieve provider.
    try:
        provider = claim_focus.provider
        if provider.resource_type != 'Practitioner':
            raise NoPractitionerError()
    except ClaimError as exc:
        raise NoPractitionerError() from exc
    # Align type and return.
    return cast(Practitioner, provider)


def claim_line_practitioner(claim_line: ClaimItem,
                            claim: Claim, claim_resources: Dict[str, Resource]) -> Practitioner:
    # Init ClaimLineFocus.
    claim_with_resources_dict = claim.dict()
    claim_with_resources_dict["contained"] = list(claim_resources.values())
    request = InsightEngineRequest(claim=Claim(**claim_with_resources_dict))
    clf = ClaimLineFocus(claim_line, request=request)
    # Get provider.
    try:
        provider = clf.provider_future
    except ClaimError as exc:
        if "Too many" in exc.message:
            raise TooManyPractitionersError() from exc
        else:
            raise NoPractitionerError() from exc
    return provider


def practitioner(claim_line: Optional[ClaimItem],
                 claim: Claim, claim_resources: Dict[str, Resource]) -> Practitioner:
    if claim_line is None:
        return claim_practitioner(claim, claim_resources)
    return claim_line_practitioner(claim_line, claim, claim_resources)


def practitioner_identifiers(provider: Practitioner) -> Dict[str, str]:
    identifiers = dict()
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
        identifiers[prov_id_type] = cast(
            Identifier,
            prov_id
        ).value.strip()

    return identifiers
