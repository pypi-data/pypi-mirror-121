from typing import Dict, Optional

from fhir.resources.claim import Claim, ClaimItem
from fhir.resources.practitioner import Practitioner

from enginelib.resources import contained_resources

from .predicates import valid_taxonomy_code, match_taxonomy_codes
from .result import SameProviderResult
from .error import NoPractitionerError, TooManyPractitionersError
from .practitioner import practitioner_identifiers, practitioner


# TODO: Remove `apikey` once versions will be implemented.
def same_provider(
    cue: Claim, 
    clue: ClaimItem, 
    oc: Claim, 
    ocl: ClaimItem, 
    apikey: Optional[str] = None,
) -> SameProviderResult:
    """
    :param apikey: just a placeholder for backward-compatibility
    """
    try:
        policy = SameProvider(cue, clue, oc, ocl)
        return policy.execute()
    except NoPractitionerError:
        return SameProviderResult.Facility
    except (KeyError, TooManyPractitionersError):
        return SameProviderResult.Error


class SameProvider:
    def __init__(self, cue: Claim, clue: ClaimItem, oc: Claim, ocl: ClaimItem):
        self.cue = cue
        self.clue = clue
        self.oc = oc
        self.ocl = ocl

        self.cue_resources = contained_resources(cue)
        self.oc_resources = contained_resources(oc)

        # The following lines may raise NoPractitionerError or TooManyPractitionersError
        self.clue_provider: Practitioner = practitioner(clue, cue, self.cue_resources)
        self.ocl_provider: Practitioner = practitioner(ocl, oc, self.oc_resources)
        self.cue_provider: Practitioner = practitioner(None, cue, self.cue_resources)
        self.oc_provider: Practitioner = practitioner(None, oc, self.oc_resources)

        self.clue_provider_ids: Dict[str, str] = practitioner_identifiers(self.clue_provider)
        self.ocl_provider_ids: Dict[str, str] = practitioner_identifiers(self.ocl_provider)
        self.cue_provider_ids: Dict[str, str] = practitioner_identifiers(self.cue_provider)
        self.oc_provider_ids: Dict[str, str] = practitioner_identifiers(self.oc_provider)

    def execute(self) -> SameProviderResult:
        # START -> Node 100: Are CLUE and OCL rendProvNPI populated?
        if 'NPI' not in self.clue_provider_ids or 'NPI' not in self.ocl_provider_ids:
            return SameProviderResult.Facility  # 100N

        # 100Y -> Node 200: Do CLUE and OCL have the same rendProvNPI?
        if self.clue_provider_ids['NPI'] == self.ocl_provider_ids['NPI']:
            return SameProviderResult.SameRendering  # 200Y

        # 200N -> Node 300: Do OCL and CLUE have the same billProvNPI?
        if self.cue_provider_ids['NPI'] == self.oc_provider_ids['NPI']:
            # 300Y -> Node 400: Are OCL and CLUE rendProvTaxonomy values
            #     both valid codes (as listed in Taxonomy crosswalk)?
            if valid_taxonomy_code(self.clue_provider_ids['TAX']) and \
                    valid_taxonomy_code(self.ocl_provider_ids['TAX']):
                # 400Y -> Node 600: Do CLUE and OCL have the same "MEDICARE
                #     SPECIALTY CODE" based on rendProvTaxonomy match to
                #     "PROVIDER TAXONOMY CODE" in Taxonomy Crosswalk?
                if match_taxonomy_codes(self.clue_provider_ids['TAX'],
                                        self.ocl_provider_ids['TAX']):
                    return SameProviderResult.Partial600Y

                # 600N
                return SameProviderResult.Partial600N

            # 400N
            return SameProviderResult.Partial400N

        # 300N -> Node 500: CLUE and OCL have the same provTaxID?
        cue_prov_tax_id = self.cue_provider_ids['34'] \
            if '34' in self.cue_provider_ids else \
            self.cue_provider_ids['24']
        oc_prov_tax_id = self.oc_provider_ids['34'] \
            if '34' in self.cue_provider_ids else \
            self.oc_provider_ids['24']

        if cue_prov_tax_id == oc_prov_tax_id:
            # 500Y -> Node 700: Are OCL and CLUE rendProvTaxonomy values
            #     both valid codes (as listed in Taxonomy crosswalk)?
            if valid_taxonomy_code(self.clue_provider_ids['TAX']) and \
                    valid_taxonomy_code(self.ocl_provider_ids['TAX']):
                # 700Y -> Node 800: Do CLUE and OCL have the same "MEDICARE
                #     SPECIALTY CODE" based on rendProvTaxonomy match to
                #     "PROVIDER TAXONOMY CODE" in Taxonomy Crosswalk?
                if match_taxonomy_codes(self.clue_provider_ids['TAX'],
                                        self.ocl_provider_ids['TAX']):
                    return SameProviderResult.Partial800Y

                # 800N
                return SameProviderResult.Partial800N

            # 700N
            return SameProviderResult.Partial700N

        # 500N
        return SameProviderResult.Different
