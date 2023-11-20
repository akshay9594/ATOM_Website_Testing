# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from test_scripts.MatrixElements_Script import test_MatrixElementData
from test_scripts.TransitionRates_Script import test_TransitionRatesData
from test_scripts.HyperfineData_Script import test_HyperfineData
from test_scripts.Nuclear_Script import test_NuclearData
from test_scripts.Energies_Script import test_EnergiesData
from test_scripts.Polarizability_Script import test_PolarizabilityData
from elements import element_data

import sys,os



def test_properties(element,gnd_truth_url,path_to_reports_dir):

    print("================================================\nTesting Results for",element,":")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print("1. Matrix Elements")
    test_MatrixElementData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n2. Transition Rates")
    test_TransitionRatesData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n3. Hyperfine Constants")
    test_HyperfineData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n4. Nuclear")
    test_NuclearData(element,driver,gnd_truth_url,path_to_reports_dir)

    print("\n5. Energies")
    test_EnergiesData(element,driver,gnd_truth_url,path_to_reports_dir)

    driver.close()

    return


gnd_truth_url = 'https://www1.udel.edu/atom/'


#element = input("Enter the element to whose data should be tested: ")

# element = element + str(charge_vals)

# print("\n2. Transition Rates")
# path_to_reports_dir = os.getcwd() + '/reports/' + element

# if(os.path.exists(path_to_reports_dir) == False):
#     os.mkdir(path_to_reports_dir)

# driver = ''

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# test_HyperfineData(element,driver,gnd_truth_url,path_to_reports_dir)

# sys.exit()

list_of_elements = element_data("","element list")

for element in list_of_elements:

    charge_vals = element_data(element)


    if(type(charge_vals)==list):
        for val in charge_vals:
            element_with_charge = element + str(val)
            path_to_reports_dir = os.getcwd() + '/reports/' + element_with_charge

            if(os.path.exists(path_to_reports_dir) == False):
                os.mkdir(path_to_reports_dir)

            test_properties(element_with_charge,gnd_truth_url,path_to_reports_dir)

    else:
        element = element + str(charge_vals)

        path_to_reports_dir = os.getcwd() + '/reports/' + element

        if(os.path.exists(path_to_reports_dir) == False):
            os.mkdir(path_to_reports_dir)

        test_properties(element,gnd_truth_url,path_to_reports_dir)

    print("\nCheck the reports/"+element,"directory for generated reports")


# sys.exit()

# element = element + str(charge_vals)

# path_to_data = os.getcwd() + '/Data/Polarizability/' + element

# path_to_reports_dir = os.getcwd() + '/reports/' + element

# test_PolarizabilityData(element,path_to_data,path_to_reports_dir)
