# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from test_scripts.MatrixElements_Script import test_MatrixElementData
from test_scripts.TransitionRates_Script import test_TransitionRatesData
from test_scripts.HyperfineData_script import test_HyperfineData
from test_scripts.Nuclear_Script import test_NuclearData
from test_scripts.Energies_Script import test_EnergiesData
from atom_charges import atom_charge

import sys,os


gnd_truth_url = 'https://www1.udel.edu/atom/'

verbosity = ''
if(len(sys.argv)>1):
    verbosity = sys.argv[1]

element = "Li"
element = element + str(atom_charge(element))

path_to_reports_dir = os.getcwd() + '/reports/' + element

if(os.path.exists(path_to_reports_dir) == False):
    os.mkdir(path_to_reports_dir)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print("Testing Results for",element,":")
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

sys.exit()


selection = input("Select property to test:\n1. Transition Rates\n2. Matrix Elements\n3. Hyperfine Constants \
                  \n4. Nuclear Data\n5. Energies Data\n")

if(selection == '1'):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    test_TransitionRatesData(element,driver,gnd_truth_url,verbosity)

elif(selection == '2'):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    test_MatrixElementData(element,driver,gnd_truth_url,verbosity)
elif(selection == '3'):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    test_HyperfineData(element,driver,gnd_truth_url,verbosity)

elif(selection == '4'):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    test_NuclearData(element,driver,gnd_truth_url,verbosity)

elif(selection == '5'):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    test_EnergiesData(element,driver,gnd_truth_url,verbosity)

else:
    print("Invalid Selection")
    sys.exit()

driver.close()

sys.exit()
