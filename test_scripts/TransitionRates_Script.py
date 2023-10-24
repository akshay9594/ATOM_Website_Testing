
from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from fetch_Gnd_Truth_Data.TransitionRates_Data import Get_TransitionRates_GndTruth_Data
from atom_charges import atom_charge
import os , ast

#Performs the actual testing
def Perform_Testing(gnd_truth_data:dict,test_data:dict,verbosity):

    if(len(gnd_truth_data.keys()) == len(test_data.keys())):
 
        states_list = list(gnd_truth_data.keys())

        mismatched_radiativeLifetimes_data = []

        mismatched_transitionRates_data = []

        States_With_Missing_RadiativeLiftimes_data = []
        States_With_Missing_TransitionRates_data = []

        for state in states_list:

            #Retrieving the test data for the state
            gnd_truth_data_tables = gnd_truth_data[state]

            test_data_tables = test_data[state]


            #Separate out the radiative lifetimes and transition rates data
            #1. Separation For Ground truth
            gndTruth_radiativeLifetimes_data = gnd_truth_data_tables[0]

            gndTruth_transitionRates_data = gnd_truth_data_tables[1:]

            
            #2. Separation for the test data
            test_ColumnHeaders = test_data_tables[0]

            test_radiativeLiftimes_data = test_data_tables[1][0]

            test_transitionRates_data = test_data_tables[1][1:]

            #Test the radiative lifetimes data. Also checks if theres missing data
            if(len(gndTruth_radiativeLifetimes_data) == len(test_radiativeLiftimes_data)):   

                diff = set(gndTruth_radiativeLifetimes_data).difference(set(test_radiativeLiftimes_data))
                if(len(diff) > 0):
                    mismatched_radiativeLifetimes_data.append([state,To_state,diff])

            else:
                States_With_Missing_RadiativeLiftimes_data.append(state)


            #Test the transition rates data
            if(len(gndTruth_transitionRates_data) == len(test_transitionRates_data)):

                for test_row in test_transitionRates_data:
                    To_state = test_row[1]
                    for gndTruth_row in gndTruth_transitionRates_data:
                        if(To_state == gndTruth_row[1]):
                            diff = set(gndTruth_row).difference(set(test_row))
                        
                            if(len(diff) > 0):
                                mismatched_transitionRates_data.append([state,To_state,diff])

            else:
                States_With_Missing_TransitionRates_data.append(state)

        # Provide details if verbosity is enabled
        if(verbosity == '-v'):
            directory = os.getcwd() + '/reports'
            report_path = os.path.join(directory, 'TransitionRates_report.txt')

            with open(report_path, 'w') as file: 
                file.write("Mismatched Radiative Lifetimes data:")
                file.write("\nFrom\tTo\t\tMismatched strings (Not displayed as in version 2)")
                for mismatched_row in mismatched_radiativeLifetimes_data:
                    state_from = mismatched_row[0]
                    state_to = mismatched_row[1]
                    file.write("\n"+state_from+"\t"+state_to+"\t\t"+str(mismatched_row[2]))

                file.write("\n==================================================================================\n")
                
                file.write("\nMismatched Transition Rates data:")
                file.write("\nFrom\tTo\t\tMismatched strings (Not displayed as in version 2)")
                for mismatched_row in mismatched_transitionRates_data:
                    state_from = mismatched_row[0]
                    state_to = mismatched_row[1]
                    diff = mismatched_row[2]

                    file.write("\n"+state_from+"\t"+state_to+"\t\t"+str(diff))
        else:
            print("Total no. of mismatched Radiative lifetimes rows: ", len(mismatched_radiativeLifetimes_data))
            print("Total no. of mismatched Transition Rates rows: ", len(mismatched_transitionRates_data))

            
    else:
        print("No. of states in the ground truth and test table are equal")
        print("Testing cannot be performed until data for missing states is added")

    return
        
        
        

def fetch_test_data_tables(driver,test_url,file_path):
     # load the web page
    driver.get(test_url)

    driver.implicitly_wait(10)

    #Get all the buttons
    btns_grid_list = driver.find_elements(By.XPATH,"//div[contains(@class, 'flex ml-4')]")

    btns_grid_text = btns_grid_list[1].text

    displayed_btns_lst = list(btns_grid_text.split("\n"))
    analyzed_btns_states = []

    TransitionRates_data_tables = {}

    #Start clicking the buttons and reproducing the tables
    for btn in displayed_btns_lst:
        btn_chars = list((btn.split("/"))[0])
        btn_chars.pop()
        btn_state = ''
        for charac in btn_chars:
           btn_state = btn_state + charac
      
        if(btn_state not in analyzed_btns_states):
            btn_state_text = "//button[text()='" + btn_state + "']"
            buttons_list = driver.find_elements(By.XPATH, btn_state_text)
            for btn in buttons_list:
                btn.click()

                #Reproduce the column titles first
                reproduced_titles = Reproduce_Column_titles(driver)
                #Reproduces the data in columns
                reproduced_data = Reproduce_Data(driver)

                TransitionRates_data_tables[btn.text] = [reproduced_titles,reproduced_data]
            
            analyzed_btns_states.append(btn_state)

    #Write the test tables to the file
    with open(file_path, 'w') as file: # saves modified html doc
        file.write(str(TransitionRates_data_tables))        





def test_TransitionRatesData(atom,driver,gnd_truth_url,verbosity):
    # Define the URL (Transition rates url for Li1)
    atom = atom + str(atom_charge("Li"))
    test_url = "https://www1.udel.edu/atom/dev/version3/transition?element="+atom

    # Get the Ground truth data
    gndTruth_TR_data_tables = Get_TransitionRates_GndTruth_Data(atom,gnd_truth_url)

    #Set the path for the test file to be written to
    directory = os.getcwd() + '/Data/TransitionRates'

    test_file = atom+'test'+'.txt'

    file_path = os.path.join(directory, test_file)

    test_data_tables = ''
    #Fetch the test data tables
    if(os.path.exists(file_path)):                      #Temporary for testing!! Needs to be removed
        f = open(file_path)
        test_data_tables = f.read()
    else:
        test_data_tables = fetch_test_data_tables(driver,test_url,file_path)

    test_data = ast.literal_eval(test_data_tables)
    
    #Perform the actual testing
   
    Perform_Testing(gndTruth_TR_data_tables, test_data,verbosity)
    print("Test Complete!!Report Generated...")