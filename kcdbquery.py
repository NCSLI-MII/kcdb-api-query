#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 Ryan Mackenzie White <ryan.white@nrc-cnrc.gc.ca>
#
# Distributed under terms of the Copyright © 2022 National Research Council Canada. license.

"""

"""

import sys
import requests
import json
import xmltodict
import csv
import argparse
from pathlib import Path

metro_areas = ["AUV", "EM", "L", "M", "PR", "T", "TF"]

base_api = "https://www.bipm.org/api/kcdb/swagger-ui/index.html?configUrl=/api/kcdb/v3/api-docs/swagger-config#/reference-data-controller"
api_url = "https://www.bipm.org/api/kcdb/swagger-ui/index.html?configUrl=/api/kcdb/v3/api-docs/swagger-config#/reference-data-controller/getMetrologyAreas"
api_swagger = "https://www.bipm.org/api/kcdb/v3/api.docs"
#https://www.bipm.org/api/kcdb/swagger-ui/index.html?configUrl=/api/kcdb/v3/api-docs/swagger-config#/reference-data-controller/getMetrologyAreas
api_domains = "https://www.bipm.org/api/kcdb/swagger-ui/index.html?configUrl=/api/kcdb/v3/api-docs/swagger-config#/reference-data-controller/getDomains"

headers = {
        'Content-type': 'application/json'
        }

#curl -X 'GET' 'https://www.bipm.org/api/kcdb/referenceData/analyte' -H 'accept:application/json':wq

api_ref = 'https://www.bipm.org/api/kcdb/referenceData/analyte' 
api_ref = 'https://www.bipm.org/api/kcdb/referenceData' 
api_search = 'https://www.bipm.org/api/kcdb/searchData'
api_quick = 'https://www.bipm.org/api/kcdb/quickData'



def getRequestExamples():
    #print(myResponse.text)
    #print(myResponse)
    #if(myResponse.ok):
    #    jData = json.loads(myResponse.content)
    #    print(jData)
    #    for key in jData:
    #        print(key, jData[key])

    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }

    parameters = {'page':0, 
            'pageSize':20, 
            'showTable':False, 
            'metrologyAreaLabel':'QM',
            'categoryLabel':'5',
            'analyteLabel':'antimony',
            'keywords':'phase OR multichannel OR water',
            'publicDateFrom':'2005-01-31',
            'publicDateTo':'2020-06-30',
            }

    #output = requests.post(f'{api_search}/chemistryAndBiology/advancedSearchChemistryAndBiology',headers=headers,data=parameters)
    #print(output.content)



    api_ref = 'https://www.bipm.org/api/kcdb/cmc/searchData/quickSearch' 
    headers= {'accept': 'application/xml',
        'Content-Type': 'application/xml'}
    xml= """<?xml version="1.0" encoding="UTF-8"?>
    <QuickSearchCriteria>
    <page>0</page>
    <pageSize>20</pageSize>
    <showTable>false</showTable>
    <keywords>phase OR test</keywords>
    <includedFilters>
    <includedFilter>cmcDomain.PHYSICS</includedFilter>
    <includedFilter>cmcBranches.Dimensional metrology</includedFilter>
    </includedFilters>
    <excludedFilters>
    <excludedFilter>cmcServices.Form</excludedFilter>
    <excludedFilter>cmcServices.Complex geometry</excludedFilter>
    </excludedFilters>
    </QuickSearchCriteria>"""

    #output = requests.post(f'{api_ref}',headers=headers,data=xml)

    #print(output.content)

    headers= {'accept': 'application/xml',
        'Content-Type': 'application/xml'}
    api_ref = 'https://www.bipm.org/api/kcdb/cmc/searchData/physics'
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <SearchCriteriaPhysics>
    <page>0</page>
    <pageSize>20</pageSize>
    <showTable>false</showTable>
    <metrologyAreaLabel>EM</metrologyAreaLabel>
    <branchLabel>EM/RF</branchLabel>
    <physicsCode>11.3.3</physicsCode>
    <keywords>phase OR multichannel OR water</keywords>
    <countries>
    <countryLabel>CH</countryLabel>
    <countryLabel>FR</countryLabel>
    </countries>
    <publicDateFrom>2005-01-31</publicDateFrom>
    <publicDateTo>2020-06-30</publicDateTo>
    </SearchCriteriaPhysics>"""

    output = requests.post(f'{api_ref}',headers=headers,data=xml)
    result = xmltodict.parse(output.content)
    print(result['ResultsPhysics']['data'])
    headers= {'Content-Type': 'application/json'}
        

    data = {
      "page": 0,
      "pageSize": 20,
      "metrologyAreaLabel": "EM",
      "showTable": False,
      "branchLabel": "EM/RF",
      "physicsCode": "11.3.3",
      "keywords": "phase OR multichannel OR water",
      "countries": [
        "CH",
        "FR",
        "JP"
      ],
      "publicDateFrom": "2005-01-31",
      "publicDateTo": "2020-06-30"
    }

    output = requests.post(f'{api_ref}',headers=headers,data=json.dumps(data))
    print(output.headers)
    result = json.loads(output.content)
    print(result['data'])
    #for key in data['data']:
    #    print(key, data[key])

# Reference data


def getRefDataPhysicsDisciplines():
    # Return reference data
    api_ref = 'https://www.bipm.org/api/kcdb/referenceData' 
    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }
    output = requests.get(f'{api_ref}/metrologyArea', headers=headers, params={"domainCode":"PHYSICS"})
    print(output.headers)
    result = json.loads(output.content)
    physics_areas = []
    for area in result["referenceData"]:
        physics_areas.append(area["label"])
    return physics_areas

def getRefDataQuantities():
    api_ref = 'https://www.bipm.org/api/kcdb/referenceData' 
    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }
    output = requests.get(f'{api_ref}/quantity', headers=headers)
    result = json.loads(output.content)
    quantities = []
    for q in result["referenceData"]:
        quantities.append(q['value'])
    return quantities

def getReferenceData(f_summary):
    api_ref = 'https://www.bipm.org/api/kcdb/referenceData' 
    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }
    output = requests.get(f'{api_ref}/metrologyArea', headers=headers, params={"domainCode":"PHYSICS"})
    
    result = json.loads(output.content)
    reference_data = {}

    reference_data['physics_areas'] = []
    f_summary.write("Physics areas\n")
    for area in result["referenceData"]:
        reference_data['physics_areas'].append(area["label"])
        f_summary.write("%s\n" % area['label'])
    
    output = requests.get(f'{api_ref}/quantity', headers=headers)
    result = json.loads(output.content)
    reference_data['quantities'] = []
    f_summary.write("Quantities\n")
    for q in result["referenceData"]:
        reference_data['quantities'].append(q['value'])
        f_summary.write("%s\n" % q['value'])

    output = requests.get(f'{api_ref}/nuclide', headers=headers)
    result = json.loads(output.content)
    reference_data['nuclides'] = []
    f_summary.write("Nuclides\n")
    for q in result["referenceData"]:
        reference_data['nuclides'].append(q['value'])
        f_summary.write("%s\n" % q['value'])
    
    return reference_data

def getPhysicsCMCData(country_code, disciplines, output_dir, f_summary):
    api_ref = 'https://www.bipm.org/api/kcdb/cmc/searchData/physics'
    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }
    data = {
      "page": 0,
      "pageSize": 20,
      "metrologyAreaLabel": None,
      "showTable": False,
      "countries": [
        country_code,
      ],
    }
    fields = None
    ntotal=0
    print(f"Query CMCs for {disciplines}")

    for area in disciplines:
        data['metrologyAreaLabel'] = area
        print(f"Request CMC for {area}")
        results=[]
        data['page'] = 0
        while True: 
            print("Page", data['page'])
            output = requests.post(f'{api_ref}',headers=headers,data=json.dumps(data))
            #print(output.headers)
            result = json.loads(output.content)
            if len(result['data']) == 0:
                break
            #print(result['data'][0])
            if data['page'] == 0:
                fields = result['data'][0].keys()
            current = len(result['data'])
            #print(fields)
            results += result['data']
            data["page"] = data["page"]+1
        nresults=len(results)
        ntotal+=nresults
        summary =f"Total records for {area}:{nresults}"
        print(summary)
        f_summary.write(summary + '\n')    
        #print(fields)
        fdomain = f'kcdb_cmc_{area}_{country_code}.csv'
        path = output_dir / fdomain
        with open(path, 'w') as f:
            writer = csv.DictWriter(f,fieldnames = fields)
            writer.writeheader()
            writer.writerows(results)
    summary = f'Total CMCs in Physics {disciplines}: {ntotal}'
    print(summary)
    f_summary.write(summary + '\n')    

def getIonizingRadiationRefData():
    api_ref = 'https://www.bipm.org/api/kcdb/referenceData' 
    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }
    output = requests.get(f'{api_ref}/nuclide', headers=headers)
    result = json.loads(output.content)
    quantities = []
    for q in result["referenceData"]:
        quantities.append(q['value'])
    return quantities

def getIonizingRadiationCMCData(country_code, output_dir, f_summary):
    api_ref = 'https://www.bipm.org/api/kcdb/cmc/searchData/radiation'
    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }
    data = {
      "page": 0,
      "pageSize": 20,
      "metrologyAreaLabel": 'RI',
      "showTable": False,
      "countries": [
        country_code,
      ],
    }
    fields = None
    ntotal=0
    print(f"Request CMC for RI")
    f_summary.write(f"Request CMC for RI\n")
    results=[]
    data['page'] = 0
    while True: 
        print("Page", data['page'])
        output = requests.post(f'{api_ref}',headers=headers,data=json.dumps(data))
        #print(output.headers)
        result = json.loads(output.content)
        if len(result['data']) == 0:
            break
        #print(result['data'][0])
        if data['page'] == 0:
            fields = result['data'][0].keys()
        current = len(result['data'])
        #print(fields)
        results += result['data']
        data["page"] = data["page"]+1
    nresults=len(results)
    ntotal+=nresults
    summary =f"Total records for RI:{nresults}"
    print(summary)
    f_summary.write(summary + '\n')    
    #print(fields)
    fdomain = f'kcdb_cmc_IR_{country_code}.csv'
    path = output_dir / fdomain
    with open(path, 'w') as f:
        writer = csv.DictWriter(f,fieldnames = fields)
        writer.writeheader()
        writer.writerows(results)
    print(f'Total CMCs in IR: {ntotal}')
    f_summary.write(f'Total CMCs in IR: {ntotal}\n')    


if __name__ == "__main__":
   
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Optional output path')
    parser.add_argument('-a', '--areas', default=[], nargs='+', help='List of Physics Areas to query')
    parser.add_argument('-r','--refonly', default=False, type=bool, help='Query reference data only')
    parser.add_argument('--ir', default=False, type=bool, help='Query Ionizing Radiation CMCs')
    parser.add_argument('--physics', default=False, type=bool, help='Query Physics CMCs')
    parser.add_argument('--country', default='CA', type=str, help='Country Code')
    args = parser.parse_args()
   
    if not args.path:
        output_dir = Path().resolve()
        print(f"Writing to current directory {output_dir.name}")
    else:
        output_dir = Path(args.path).resolve()
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"Creating output directory {output_dir.name}")
        print(f"Writing to directory {output_dir.name}")
    f_summary = open(output_dir / 'kcdb_query_summary.txt', 'w')
    reference_data = getReferenceData(f_summary)
    print("Obtain CMCs for the following physics areas")
    print(reference_data['physics_areas'])
    
    if args.refonly is True:
        sys.exit(0)
    if args.ir is True:
        getIonizingRadiationCMCData(args.country, output_dir, f_summary)
    if args.physics is True:
        if len(args.areas) > 0:
            print(f"Querying Physics CMCs for {args.areas}")
            getPhysicsCMCData(args.country, args.areas, output_dir, f_summary)
        else:
            print(f"Querying Physics CMCs for all areas {reference_data['physics_areas']}")
            getPhysicsCMCData(args.country, reference_data['physics_areas'], output_dir, f_summary)

    f_summary.close()
    
