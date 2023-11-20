
import requests
import json
import sys

import os,sys
from fetch_Gnd_Truth_Data.Polarizability_Data import fetchPolarizabilityData


query = """
query GetElementQuery($title: String) {
  element(title: $title) {
    id
    title
    titleDisplay
    NISTASDTitle
    isMatrixElements
    isTransitionRates
    isEnergies
    isNuclears
    isHyperfineConstants
    isPolarizabilities
    isStaticPolarizabilities
    isHCIEnergies
    isHCITransitions
    dynamicPolarizabilities {
      state
      wavelength
      alpha
      __typename
    }
    matrixElements {
      stateOne
      initialEnergy
      __typename
    }
    __typename
  }
}
"""

def fetch_test_data()->dict:
# we have imported the requests modul


    # defined a URL variable that we will be
    # using to send GET or POST requests to the API
    url = "https://atom.ece.udel.edu/graphql"
    

    response = requests.post(url=url, json={"query": query})

    if response.status_code != 200:
        print("No response!Check query\nStatus code: ", response.status_code)
        sys.exit()


    response_String =  response.content.decode('utf-8')
    json_obj = json.loads(response_String)
    data_json = list(json_obj.values())
    data = data_json.pop()
    response_data = (dict(data['element']))
    polData_list = list(response_data['dynamicPolarizabilities'])

    test_data = {}
    states_list = []
    for dict_entry in polData_list:
        state = dict_entry['state']
        if(state not in states_list):
            test_data[state] = []
    
    for dict_entry in polData_list:
        state = dict_entry['state']
        wavelength = dict_entry['wavelength']
        alpha = dict_entry['alpha']
        list_wavelength = test_data[state]
        list_wavelength.append((wavelength,alpha))

    return test_data
    


def test_PolarizabilityData(element,path_to_data_dir,path_to_reports_dir):

    #Get the ground truth data (Data from the physicists)
    StaticPol_GndTruth_Data, Pol_GndTruth_Data = fetchPolarizabilityData(path_to_data_dir)
    print(Pol_GndTruth_Data.keys())

    Pol_test_Data = fetch_test_data()
    print(Pol_test_Data.values())

    return