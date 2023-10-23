# import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from test_scripts.MatrixElements_Script import test_MatrixElementData
from test_scripts.TransitionRates_Script import test_TransitionRatesData
from test_scripts.HyperfineData_script import test_HyperfineData
from test_scripts.Nuclear_Script import test_NuclearData
from test_scripts.Energies_Script import test_EnergiesData


import sys


gnd_truth_url = 'https://www1.udel.edu/atom/'

verbosity = ''
if(len(sys.argv)>1):
    verbosity = sys.argv[1]

element = "Li"


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
