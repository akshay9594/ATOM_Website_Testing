


from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from atom_charges import atom_charge
from fetch_Gnd_Truth_Data.Energies_Data import Get_Energies_data
import os,ast


def perform_testing(gnd_truth_table:list, test_table:list, verbosity):

    Mismatched_Rows = []
    for test_row in test_table:
        test_state = test_row[0]
        for gnd_truth_row in gnd_truth_table:
            gndTruth_state = gnd_truth_row[0]
            if(test_state == gndTruth_state):
                diff = set(gnd_truth_row).difference(set(test_row))

                if(len(diff) > 0):
                    Mismatched_Rows.append([gnd_truth_row,test_row,diff])


    if(len(Mismatched_Rows)==0):
        print("No Mismatches between the test and ground truth tables")
    else:
        if(verbosity == '-v'):
            print("Gnd Truth\t\t\t\tTest\t\t\t\tMismatches(Not displayed as in version 2)")
            for row in Mismatched_Rows:
                print(row[0],"\t",row[1],"\t",row[2])
        else:
            print("There are ", len(Mismatched_Rows), " number of mismatched rows")

    



def test_EnergiesData(atom,driver,gnd_truth_url,verbosity):

    atom = atom + str(atom_charge("Li"))
    # Define the URL (Transition rates url for Li1)
    url = "https://www1.udel.edu/atom/dev/version3/energy?element=" + atom

    # load the web page
    driver.get(url)

    driver.implicitly_wait(10)

    #Get the ground truth
    gnd_truth_data_tables = Get_Energies_data(atom,gnd_truth_url)

    directory = os.getcwd() + '/Data/Energies'

    test_file = atom+'test'+'.txt'

    file_path = os.path.join(directory, test_file)

    test_data_tables = ''
    test_table_column_titles = ''


    if(os.path.exists(file_path)):
        f = open(file_path)
        test_data_tables = f.read()
        test_data_tables = ast.literal_eval(test_data_tables)
    else:
         #Fetch the tables from the test version: Version 3
        test_table_column_titles = Reproduce_Column_titles(driver)
        test_data_tables = Reproduce_Data(driver)
        test_data_tables.insert(0,test_table_column_titles)
        with open(file_path, 'w') as file: 
            file.write(str(test_data_tables))
    
    perform_testing(gnd_truth_data_tables,test_data_tables,verbosity)