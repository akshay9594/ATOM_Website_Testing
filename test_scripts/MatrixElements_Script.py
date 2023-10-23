
from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from fetch_Gnd_Truth_Data.Matrix_Elements_Data import Get_MatrixElements_data
from atom_charges import atom_charge
import os,ast


def Perform_Testing(gnd_truth_data:dict,test_data:dict,verbosity):
    gnd_truth_states_list = list(gnd_truth_data.keys())
    test_data_states_list = list(test_data.keys())

    missing_states = []
    for state in test_data_states_list:
        if((state in gnd_truth_states_list) == False):
            missing_states.append(state)

    print("\n==============================Results=====================================")
    mismatched_data = []
    if(len(missing_states)>0):
        print("Number of missing states = ", len(missing_states))
        print("Further Consistency Check aborted!")
    else:
        print("No Missing states..")
        for state in gnd_truth_states_list:
            gnd_truth_frame = gnd_truth_data[state]
            test = test_data[state]
            test.remove(test[0])
            test_data_frame = test.pop()
        
            for test_row in test_data_frame:
                    To_state = test_row[1]
                    for gndTruth_row in gnd_truth_frame:
                        if(To_state == gndTruth_row[1]):
                            diff = set(gndTruth_row).difference(set(test_row))
                        
                            if(len(diff) > 0):
                                mismatched_data.append([state,To_state,diff])


    if(len(mismatched_data) > 0):
        
        if(verbosity == '-v'):
            print("From\tTo\t\tMismatched strings (Not displayed as in version 2)")
            for mismatched_row in mismatched_data:
                state_from = mismatched_row[0]
                state_to = mismatched_row[1]
                diff = mismatched_row[2]

                print(state_from,"\t",state_to,"\t\t",diff)
        else:
            print("There are",len(mismatched_data), "mismatched rows")

    else:
        print("No mismatched Data!!")
    print("==========================================================================\n")

    return



def fetch_test_data_tables(driver,test_url,file_path):
     # load the web page
    driver.get(test_url)

    driver.implicitly_wait(20)

    num_clicks_on_More_states = 3

    while(num_clicks_on_More_states>0):

        btn_state_text = "//button[text()='More states']"
        More_states_btn = driver.find_element(By.XPATH, btn_state_text)
        More_states_btn.click()
        num_clicks_on_More_states = num_clicks_on_More_states - 1

    btns_grid = driver.find_element(By.XPATH,"//div[contains(@class, 'grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2')]")

    btns_grid_text = btns_grid.text

    # # #List of buttons to click
    # # buttons = ['2s']

    displayed_btns_lst = list(btns_grid_text.split("\n"))
    analyzed_btns_states = []

    MatrixElements_data_tables = {}

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

                MatrixElements_data_tables[btn.text] = [reproduced_titles,reproduced_data]
            
            analyzed_btns_states.append(btn_state)
        
    with open(file_path, 'w') as file: # saves modified html doc
        file.write(str(MatrixElements_data_tables))



def test_MatrixElementData(element,driver,gnd_truth_url,verbosity):

    #Fetch the ground truth data
    gnd_truth_data_tables = Get_MatrixElements_data(element,gnd_truth_url)


    element = element + str(atom_charge("Li"))
     # Define the URL (Transition rates url for Li1)
    test_url = "https://www1.udel.edu/atom/dev/version3/matrix?element="+element


    directory = os.getcwd() + '/Data/MatrixElements'

    test_file = element+'test'+'.txt'

    file_path = os.path.join(directory, test_file)

    test_data_tables = ''
    if(os.path.exists(file_path)):
        f = open(file_path)
        test_data_tables = f.read()
        test_data_tables = ast.literal_eval(test_data_tables)
    else:
        test_data_tables = fetch_test_data_tables(driver,test_url,file_path)
    
    Perform_Testing(gnd_truth_data_tables,test_data_tables,verbosity)

    
    # for btn in MatrixElements_data_tables.keys():
    #     print('state=',btn,"\n", MatrixElements_data_tables[btn])
    #     print ("********************************************************************")