#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

base_folder = os.getcwd()
if base_folder.endswith('same_provider'):
    base_folder = os.path.dirname(base_folder)
if base_folder.endswith('tests') or base_folder.endswith('matchers'):
    base_folder = os.path.dirname(base_folder)
if base_folder.endswith('enginelib'):
    base_folder = os.path.dirname(base_folder)

base_claim_folder = os.path.join(base_folder, 'tests', 'same_provider', 'input')
test_cases_folder = os.path.join(base_claim_folder, 'generated')
os.makedirs(test_cases_folder, exist_ok=True)

sys.path.append(base_folder)

import json
import csv
import copy
from typing import cast, List, Optional
import datetime as dt

from fhir.resources.identifier import Identifier
from fhir.resources.quantity import Quantity
from fhir.resources.coverage import Coverage
from fhir.resources.period import Period
from fhir.resources.practitioner import Practitioner
from fhir.resources.claim import Claim, ClaimInsurance, ClaimItem, ClaimCareTeam
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coverage import CoverageClass
from fhir.resources.patient import Patient
from testcases import dsl


# Identifier

def identifier(value: str, _type: str, system: str = None) -> Identifier:
    _id = Identifier()
    _id.system = system
    _id.value = value
    # noinspection PyProtectedMember
    _id.type = dsl._codeableconcept(code=_type, system=system)
    return _id


# Practitioner

def practitioner(_id: str = "practitioner-1", 
                 tax_id: str = None, 
                 npi: str = None, 
                 taxonomy: str = None) -> Practitioner:
    p = Practitioner.construct()
    
    p.identifier = list()
    if tax_id is not None:
        # noinspection HttpUrlsUsage
        s = "https://ediacademy.com/blog/x12-n104-identification-code-qualifier-code-identifying-party-code/"
        new_id = identifier(value=tax_id, _type='34', system=s)
        p.identifier.append(new_id)
    if npi is not None:
        # noinspection HttpUrlsUsage
        s = "http://terminology.hl7.org/2.1.0/CodeSystem-v2-0203.html"
        new_id = identifier(value=npi, _type='NPI', system=s)
        p.identifier.append(new_id)
    if taxonomy is not None:
        # noinspection HttpUrlsUsage
        s = "https://nucc.org/index.php/code-sets-mainmenu-41/provider-taxonomy-mainmenu-40/csv-mainmenu-57"
        new_id = identifier(value=taxonomy, _type='TAX', system=s)
        p.identifier.append(new_id)
        
    p.id = _id
    return p


# The only patient for the claims

john = dsl.patient(
    last="Doe",
    first="John",
    _id="6985471",
    street1="417 N. Decatur Rd.",
    city="Atlanta",
    state="GA",
    postal_code="30307"
)


# Coverage

def coverage_class(code: str) -> CodeableConcept:
    # noinspection HttpUrlsUsage
    system = "http://hl7.org/fhir/ValueSet/coverage-class"
    # noinspection PyProtectedMember
    return dsl._codeableconcept(code=code, system=system)


def get_coverage(patient_id: str, order: int = 1, subscriber_id: str = None, tpe: str = 'Medicare',
                 group: str = None, relationship: str = 'self') -> Coverage:
    if subscriber_id is None:
        subscriber_id = patient_id
        relationship = 'self'
    medicare_cov = dsl.coverage(
        tpe=tpe,
        order=order,  # primary, secondary, tertiary, etc
        relationship=relationship,
        sid=subscriber_id,
        patientid=patient_id,
    )

    if group is not None:
        medicare_cov.class_fhir = list()
        medicare_cov.class_fhir.append(CoverageClass(type=coverage_class('group'), value=group))

    return medicare_cov


def medicare_coverage(patient_id: str, order: int = 1, subscriber_id: str = None, 
                      group: str = None, relationship: str = 'self') -> Coverage:
    return get_coverage(patient_id, order, subscriber_id, 'Medicare', group, relationship)


# Insurance

def get_insurance(ins_coverage: Coverage) -> ClaimInsurance:
    return ClaimInsurance(sequence=1, focal=True, coverage=dsl.reference(ins_coverage.id))


standard_coverage = medicare_coverage(patient_id=john.id, group='12654')


# Base claim

cache = dict()


def read_base_claim(filename: str = None):
    filename = filename or os.path.join(base_claim_folder, 'base_claim_for_same_provider_tests.json')
    with open(filename) as f:
        data = json.load(f)
        claim = Claim(**data)
        claim_line = cast(ClaimItem, claim.item[0])
        claim.item = list()
    cache['claim'] = claim
    cache['claim_line'] = claim_line


def base_claim() -> Claim:
    if not cache:
        read_base_claim()
    return copy.deepcopy(cache['claim'])


def get_claim(_id: str, providers: List[Practitioner], lines: List[ClaimItem],
              pat: Patient = john, cov: Coverage = standard_coverage, 
              diag: str = 'M26.05') -> Claim:
    """
    Assumes first provider in the list is the billing provider (referenced by claim.provider)
    """
    claim = base_claim()
    claim.identifier = dsl.claim_num(_id)
    claim.patient = dsl.reference(pat.id)
    claim.provider = dsl.reference(providers[0].id)
    
    ins = get_insurance(cov)
    claim.insurance = [ins]
    
    claim.diagnosis = [dsl.diagnosis(diag)]
    claim.contained = [pat, cov]

    claim.careTeam = list()
    for i, provider in enumerate(providers):
        claim.careTeam.append(ClaimCareTeam(provider=dsl.reference(provider.id), sequence=(i+1)))
        # noinspection PyTypeChecker
        claim.contained.append(provider)
    
    claim.item = lines
    for i, line in enumerate(lines):
        line.sequence = i + 1
        
    return claim
    

def save_claim(claim: Claim, name: str):
    filename = os.path.join(test_cases_folder, name)
    with open(filename, 'w') as f:
        js_plain = claim.json()
        js = json.loads(js_plain)
        json.dump(js, f, indent=2)


# Base claim line

def base_claim_line() -> ClaimItem:
    if not cache:
        read_base_claim()
    return copy.deepcopy(cache['claim_line'])


def get_claim_line(procedure_code: str = '70140', 
                   modifiers: List[str] = None,
                   provider_index: int = 2,
                   units: int = 1, 
                   dos: str = '2020-05-20') -> ClaimItem:

    modifiers = modifiers or list()

    claim_line = base_claim_line()
    # noinspection PyProtectedMember
    claim_line.productOrService = dsl._codeableconcept(
        code=procedure_code, 
        system='https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets/Alpha-Numeric-HCPCS'
    )
    claim_line.modifier = [dsl.modifier(mod) for mod in modifiers]
    claim_line.quantity = Quantity(value=units)

    # Either set servicedDate or servicedPeriod:
    claim_line.servicedDate = None
    claim_line.servicedPeriod = Period(
        start=dt.date.fromisoformat(dos),
        end=dt.date.fromisoformat(dos)
    )

    claim_line.careTeamSequence = [provider_index]
    return claim_line


# Creating `.json` files from `test_plan.csv`
claim_number = 0


def claim_from_providers_info(billProvNPI: str, provTaxID: str, rendProvNPI: str, rendProvTaxonomy: Optional[str]):
    global claim_number
    claim_number += 1
    
    # billProvTaxonomy is irrelevant according to the tree in the specification,
    #     so we just pick '207NI0002X'
    bill_provider = practitioner(
        _id='practitioner-1', 
        npi=billProvNPI, 
        tax_id=provTaxID, 
        taxonomy='207NI0002X'
    )
    
    # SSN or Employer's Identification Number of renderingProvider is irrelevant 
    #     according to the tree in the specification, so we pick '6673890'
    rend_provider = practitioner(
        _id='practitioner-2', 
        npi=rendProvNPI,
        tax_id='6673890', 
        taxonomy=rendProvTaxonomy
    )
    
    claim = get_claim(
        _id=f'CLAIM999{claim_number:04}', 
        providers=[bill_provider, rend_provider], 
        lines=[get_claim_line()]
    )
    
    return claim


def run():
    test_plan_csv = os.path.join(base_folder, 'tests', 'same_provider', 'test_plan.csv')
    with open(test_plan_csv) as f:
        rows = csv.reader(f)
        _header = next(rows)
        for row in rows:
            values = [(value if value else None) for value in row]
            cue_billProvNPI, cue_provTaxID, clue_rendProvNPI, clue_rendProvTaxonomy = values[0:4]
            oc_billProvNPI, oc_provTaxID, ocl_rendProvNPI, ocl_rendProvTaxonomy = values[4:8]
            result_type, result_text = values[8:]

            cue = claim_from_providers_info(cue_billProvNPI, cue_provTaxID, clue_rendProvNPI, clue_rendProvTaxonomy)
            save_claim(cue, name=f'CLUE_{result_type}.json')
            
            oc = claim_from_providers_info(oc_billProvNPI, oc_provTaxID, ocl_rendProvNPI, ocl_rendProvTaxonomy)
            save_claim(oc, name=f'OCL_{result_type}.json')


if __name__ == '__main__':
    run()
