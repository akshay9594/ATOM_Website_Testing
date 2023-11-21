
from selenium.webdriver.common.by import By
from Reproduce_tables import Reproduce_Column_titles,Reproduce_Data
from fetch_Gnd_Truth_Data.Atomic_Data import Get_Atomic_data

import os,ast,itertools

#Splits a list into two lists at a specific element
def split_list(lst, val):
    return [list(group) for k, 
            group in
            itertools.groupby(lst, lambda x: x==val) if not k]


def Remove_Empty_Rows(test_table):

    mismatched_data = []
    empty_rows = 0

    row_indices_to_remove = []
    test_table_without_empty_rows = []
    for i in range(0,len(test_table)):
        test_row = test_table[i]
        if(test_row[0] == '' and all(i == test_row[0] for i in test_row)):
            empty_rows = empty_rows + 1
        else:
            test_table_without_empty_rows.append(test_row)

    return test_table_without_empty_rows


def perform_testing(gnd_truth_table:tuple, test_table:tuple, path_to_reports_dir:str,Column_titles:list):

    #Get the groud truth tables
    gndTruth_Energy_table = gnd_truth_table[0]
    gndTruth_TREnergy_table = gnd_truth_table[1]


    #Get the test tables
    test_Energy_table = test_table[0]
    test_TREnergy_table = test_table[1]

    #Remove empty rows if any from the test tables
    # test_Energy_table = Remove_Empty_Rows(test_Energy_table)
    # test_TREnergy_table = Remove_Empty_Rows(test_TREnergy_table)

    for i in range(0,len(Column_titles)):
        Column_titles[i] = Column_titles[i].replace("\n","").replace("Ref","")

    Column_titles = split_list(Column_titles,"Lifetime (s)")

    Column_titles[0].append("Lifetime (s)")
    Energies_Column_titles =  Column_titles[0]
    TransitionEnergy_Column_titles = Column_titles[1]

    mismatched_Energies_data = []
    for gndTruth_row, test_row in zip(gndTruth_Energy_table,test_Energy_table):
        
        state = gndTruth_row[0]
        diff = set(gndTruth_row).difference(set(test_row))
        
        if(len(diff) > 0):
            diff_data_to_report = []
            diff = list(diff)
            
            for j in range(0,len(diff)):
                value_v2 = diff[j]
                id = gndTruth_row.index(value_v2)
                Column_title = (Energies_Column_titles[id]).replace("\n","")
                Column_title = Column_title.replace("info","")
                value_v3 = test_row[id]
                diff_data_to_report.append([value_v3,value_v2,Column_title])
            mismatched_Energies_data.append([state,diff_data_to_report])


    mismatched_TREnergies_data = []
    for gndTruth_row, test_row in zip(gndTruth_TREnergy_table,test_TREnergy_table):
        
        Transition = gndTruth_row[0]
        diff = set(gndTruth_row).difference(set(test_row))
        
        if(len(diff) > 0):
            diff_data_to_report = []
            diff = list(diff)
            
            for j in range(0,len(diff)):
                value_v2 = diff[j]
                id = gndTruth_row.index(value_v2)
                Column_title = (TransitionEnergy_Column_titles[id]).replace("\n","")
                Column_title = Column_title.replace("info","")
                value_v3 = test_row[id]
                diff_data_to_report.append([value_v3,value_v2,Column_title])
            mismatched_TREnergies_data.append([Transition,diff_data_to_report])

    report_path = os.path.join(path_to_reports_dir, 'Atomic_report.txt')

    with open(report_path, 'w') as file: 
        if(len(mismatched_Energies_data)==0):
            file.write("No mismatches between the ground truth and test Energies data")
        else:
            file.write("Mismatches in the Energies Table:\n")
            file.write("\nState\t\t\tColumn\t\t\t\t\t\tValue in V3(Test)\t\t\tValue in V2(Ground Truth)")
            file.write("\n--------------------------------------------------------------------------------------------------------------")
            for mismatched_row in mismatched_Energies_data:
                state = mismatched_row[0]
                diff_data_to_report = mismatched_row[1]
            
                for row in diff_data_to_report:
                    value_v3 = row[0]
                    value_v2 = row[1]
                    Column_title = row[2]
                    file.write("\n"+state+"\t\t"+Column_title+"\t\t\t\t\t\t\t"+value_v3+"\t\t\t\t\t\t\t\t"+value_v2)

        file.write("\n=================================================================================================================\n\n")

        if(len(mismatched_TREnergies_data)==0):
            file.write("No mismatches between the ground truth and test Transition Energies data")
        else:
            file.write("Mismatches in the Transition Energies Table:\n")
            file.write("Transition\t\t\tColumn\t\t\t\t\t\tValue in V3(Test)\t\t\tValue in V2(Ground Truth)")
            file.write("\n--------------------------------------------------------------------------------------------------------------")
            for mismatched_row in mismatched_TREnergies_data:
                Transition = mismatched_row[0]
                diff_data_to_report = mismatched_row[1]
            
                for row in diff_data_to_report:
                    value_v3 = row[0].replace("\n","")
                    value_v2 = row[1].replace("\n","")
                    Column_title = row[2]
                    if("Matrix element" in Column_title or "Transition rate" in Column_title):
                        file.write("\n"+Transition+"\t\t"+Column_title+"\t\t\t\t"+value_v3+"\t\t\t\t\t\t\t"+value_v2)
                    else:
                        file.write("\n"+Transition+"\t\t"+Column_title+"\t\t\t\t\t\t"+value_v3+"\t\t\t\t\t\t\t"+value_v2)

        file.write("\n--------------------------------------------------------------------------------------------------------------")

    return



#Fetching the data tables and performing the testing
def test_AtomicData(element,driver,gnd_truth_url,path_to_reports_dir):

    #Get the ground truth
    gndTruth_Energy_Table, gndTruth_TREnergy_Table = Get_Atomic_data(element,gnd_truth_url)

    if(gndTruth_Energy_Table == [] or gndTruth_TREnergy_Table == []):
        print("Gnd Truth Data not available!Property not tested...")
        return

    # # Define the URL (Transition rates url for Li1)
    url = "https://www1.udel.edu/atom/dev/version3/atomic?element=" + element

    # load the web page
    driver.get(url)

    driver.implicitly_wait(10)

    directory = os.getcwd() + '/Data/Atomic'

    test_file = element+'test'+'.txt'

    file_path = os.path.join(directory, test_file)

    test_data_tables = ''
    test_table_column_titles = ''

    #Fetch the tables from the test version: Version 3
    #The table column titles and the actual data are reproduced separately
    if(os.path.exists(file_path)):
        f = open(file_path)
        test_data_tables = f.read()
        test_data_tables = ast.literal_eval(test_data_tables)
        test_table_column_titles = test_data_tables.pop(0)
    else:
        test_table_column_titles = Reproduce_Column_titles(driver)
        test_data_tables = Reproduce_Data(driver)
        test_data_tables.insert(0,test_table_column_titles)
        if(test_table_column_titles==[] or test_data_tables==[]):
            print("Test Data not available!Property not tested...")
            return
        
        with open(file_path, 'w') as file: 
            file.write(str(test_data_tables))

    Test_Energy_Table = []
    Test_TREnergy_Table = []

   
    #Separate out the Energies table and the Transition Energies table
    for test_row in test_data_tables:
        temp_list = [x for x in test_row[0]]
        Transition_Present = False
        for ch in temp_list:
            if(ord(ch) == 8722):
                Transition_Present = True
                break
        if(Transition_Present):
            Test_TREnergy_Table.append(test_row)     
        else:
            Test_Energy_Table.append(test_row)

    #Perform the testing
    perform_testing((gndTruth_Energy_Table,gndTruth_TREnergy_Table),(Test_Energy_Table,Test_TREnergy_Table),path_to_reports_dir,test_table_column_titles)