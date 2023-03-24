#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 Ryan Mackenzie White <ryan.white@nrc-cnrc.gc.ca>
#
# Distributed under terms of the Copyright © 2022 National Research Council Canada. license.

"""

"""

import requests
import json
import xmltodict
import csv

metro_areas = ["AUV", "EM", "L", "M", "PR", "T", "TF"]

base_api = "https://www.bipm.org/api/kcdb/swagger-ui/index.html?configUrl=/api/kcdb/v3/api-docs/swagger-config#/reference-data-controller"
api_url = "https://www.bipm.org/api/kcdb/swagger-ui/index.html?configUrl=/api/kcdb/v3/api-docs/swagger-config#/reference-data-controller/getMetrologyAreas"
api_swagger = "https://www.bipm.org/api/kcdb/v3/api.docs"
#https://www.bipm.org/api/kcdb/swagger-ui/index.html?configUrl=/api/kcdb/v3/api-docs/swagger-config#/reference-data-controller/getMetrologyAreas
api_domains = "https://www.bipm.org/api/kcdb/swagger-ui/index.html?configUrl=/api/kcdb/v3/api-docs/swagger-config#/reference-data-controller/getDomains"

headers = {
        'Content-type': 'application/json'
        }

#curl -X 'GET' 'https://api-bipm.timsoft.com/api/kcdb/referenceData/analyte' -H 'accept:application/json':wq

api_ref = 'https://api-bipm.timsoft.com/api/kcdb/referenceData/analyte' 
api_ref = 'https://api-bipm.timsoft.com/api/kcdb/referenceData' 
api_search = 'https://api-bipm.timsoft.com/api/kcdb/searchData'
api_quick = 'https://api-bipm.timsoft.com/api/kcdb/quickData'



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



    api_ref = 'https://api-bipm.timsoft.com/api/kcdb/cmc/searchData/quickSearch' 
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
    api_ref = 'https://api-bipm.timsoft.com/api/kcdb/cmc/searchData/physics'
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
    api_ref = 'https://api-bipm.timsoft.com/api/kcdb/referenceData' 
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
    api_ref = 'https://api-bipm.timsoft.com/api/kcdb/referenceData' 
    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }
    output = requests.get(f'{api_ref}/quantity', headers=headers)
    result = json.loads(output.content)
    quantities = []
    for q in result["referenceData"]:
        quantities.append(q['value'])
    return quantities

def getPhysicsCMCData(disciplines):
    api_ref = 'https://api-bipm.timsoft.com/api/kcdb/cmc/searchData/physics'
    headers = {'accept': 'application/json',
            'Content-Type': 'application/json'
            }
    data = {
      "page": 0,
      "pageSize": 20,
      "metrologyAreaLabel": None,
      "showTable": False,
      "countries": [
        "CA",
      ],
    }
    fields = None
    ntotal=0
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
        #print(fields)
        fdomain = f'kcdb_cmc_{area}.csv'
        with open(fdomain, 'w') as f:
            writer = csv.DictWriter(f,fieldnames = fields)
            writer.writeheader()
            writer.writerows(results)
    print(f'Total CMCs in Physics {disciplines}: {ntotal}')
if __name__ == "__main__":
    
    physicsAreas = getRefDataPhysicsDisciplines()
    quantities = getRefDataQuantities()
    #print(physicsAreas)
    #print(quantities)

    getPhysicsCMCData(metro_areas)
    
