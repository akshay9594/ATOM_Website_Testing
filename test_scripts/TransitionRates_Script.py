
from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from fetch_Gnd_Truth_Data.TransitionRates_Data import Get_TransitionRates_GndTruth_Data
from atom_charges import atom_charge
import os , ast




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

            if(len(gndTruth_radiativeLifetimes_data) == len(test_radiativeLiftimes_data)):   

                diff = set(gndTruth_radiativeLifetimes_data).difference(set(test_radiativeLiftimes_data))
                if(len(diff) > 0):
                    mismatched_radiativeLifetimes_data.append([state,To_state,diff])

            else:
                States_With_Missing_RadiativeLiftimes_data.append(state)


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

        if(verbosity == '-v'):
            print("Mismatched Radiative Lifetimes data:")
            print("From\tTo\t\tMismatched strings (Not displayed as in version 2)")
            for mismatched_row in mismatched_radiativeLifetimes_data:
                state_from = mismatched_row[0]
                state_to = mismatched_row[1]
                print(state_from,"\t",state_to,"\t\t",mismatched_row[2])

            print("==================================================================================")
            print("Mismatched Transition Rates data:")
            print("From\tTo\t\tMismatched strings (Not displayed as in version 2)")
            for mismatched_row in mismatched_transitionRates_data:
                state_from = mismatched_row[0]
                state_to = mismatched_row[1]
                diff = mismatched_row[2]

                print(state_from,"\t",state_to,"\t\t",diff)
        else:
            print("Total no. of mismatched Radiative lifetimes rows: ", len(mismatched_radiativeLifetimes_data))
            print("Total no. of mismatched Transition Rates rows: ", len(mismatched_transitionRates_data))

            
    else:
        print("No. of states in the ground truth and test table are equal")
        print("Testing cannot be performed until data for missing states is added")

    return
        
        
        
    #Get_RadiativeLifeTimes_test_data(test_data_values)

def fetch_test_data_tables(driver,test_url,file_path):
     # load the web page
    driver.get(test_url)

    driver.implicitly_wait(10)

    btns_grid_list = driver.find_elements(By.XPATH,"//div[contains(@class, 'flex ml-4')]")

    btns_grid_text = btns_grid_list[1].text

    displayed_btns_lst = list(btns_grid_text.split("\n"))
    analyzed_btns_states = []

    TransitionRates_data_tables = {}

    #displayed_btns_lst = ['3s1/2']                                   #Downloading data for 1 btn!!Temporary for testing!! Needs to be removed

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

    with open(file_path, 'w') as file: # saves modified html doc
        file.write(str(TransitionRates_data_tables))        





def test_TransitionRatesData(atom,driver,gnd_truth_url,verbosity):
    # Define the URL (Transition rates url for Li1)
    atom = atom + str(atom_charge("Li"))
     # Define the URL (Transition rates url for Li1)
    test_url = "https://www1.udel.edu/atom/dev/version3/transition?element="+atom

    directory = os.getcwd() + '/Data/TransitionRates'

    test_file = atom+'test'+'.txt'

    file_path = os.path.join(directory, test_file)

    gndTruth_TR_data_tables = Get_TransitionRates_GndTruth_Data(atom,gnd_truth_url)

    test_data_tables = ''
    if(os.path.exists(file_path)):                      #Temporary for testing!! Needs to be removed
        f = open(file_path)
        test_data_tables = f.read()
    else:
        test_data_tables = fetch_test_data_tables(driver,test_url,file_path)

    test_data = ast.literal_eval(test_data_tables)
    
    print("\n==============================Results=====================================")
    Perform_Testing(gndTruth_TR_data_tables, test_data,verbosity)
    print("==========================================================================\n")