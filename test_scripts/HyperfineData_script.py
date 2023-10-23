

from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from atom_charges import atom_charge
from fetch_Gnd_Truth_Data.Hyperfine_Data import Get_Hyperfine_data
import os,ast



def process_test_tables(test_tables:list):

    for i in range(0,len(test_tables)):
        row = test_tables[i]
        if(row[3] != '' ):
            row[3] = row[3].replace("\nRef", "")
    
        if(row[2] != '' ):
            row[2] = row[2].replace("\nRef", "")
        test_tables[i] = row

    return test_tables

def perform_testing(gndTruth_Column_titles, gndTruth_table, test_Column_titles, test_table):

    mismatched_data = []
    empty_rows = 0

    for test_row in test_table:
        state = test_row[1]
        if(state == ''):
            empty_rows = empty_rows + 1
            test_table.remove(test_row)

    for gndTruth_row, test_row in zip(gndTruth_table,test_table):
        state = test_row[1]
        diff = set(gndTruth_row).difference(set(test_row))

        if(len(diff) > 0):
            if(len(diff) == 1):
                diff = diff.pop()
                diff = diff.replace(" ", "")
                if(diff != test_row[0]):
                    mismatched_data.append([state,diff])
            else:
                mismatched_data.append([state,diff])


    print("There is ", empty_rows, " number of empty rows in the test data\nMismatched data:\n")
    if(len(mismatched_data)==0):
        print("No mismatches between the ground truth and test data")
    else:
        print("state\t\tMissing/Mismatched strings (Not displayed as in version 2)")
        for mismatched_row in mismatched_data:
            print(mismatched_row[0],"\t\t",mismatched_row[1])


def test_HyperfineData(atom,driver,gnd_truth_url,verbosity):
 
    atom = atom + str(atom_charge("Li"))
     # Define the Test URL (Version 3)
    test_url = "https://www1.udel.edu/atom/dev/version3/hyperfine?element="+atom

    #Fetch the ground truth data: Version 2 data
    gndTruth_Table_Columns_titles, gndTruth_Table = Get_Hyperfine_data(atom,gnd_truth_url)

    # load the web page
    driver.get(test_url)

    driver.implicitly_wait(10)


    directory = os.getcwd() + '/Data/Hyperfine'

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
        with open(file_path, 'w') as file: 
            file.write(str(test_data_tables))

    test_data_tables = process_test_tables(test_data_tables)

    print("\n==============================Results=====================================")
    perform_testing(gndTruth_Table_Columns_titles,gndTruth_Table,test_table_column_titles,test_data_tables)
    print("==========================================================================\n")
   

    

    







