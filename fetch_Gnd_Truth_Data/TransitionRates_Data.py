import sys,os
from atom_charges import atom_charge

sys.path.append(os.getcwd()+'/fetch_Gnd_TRuth_Data')

import utils

data_type = 'TransitionRates'

def fetch_TransitionRates_tables(atom,url):
     
    file = atom + "TranAuto.html"
    url = url + file
    TR_tables_GndTruth = utils.get_gnd_truth_tables(atom,url,data_type,'version2')
    return TR_tables_GndTruth


#Consider only the ground truth TR data that is displayed on the website for testing
def getRelevant_TR_data(TR_table):
    # 0,1,4,7,10,13

    for i in range(0,len(TR_table)):
        row = TR_table[i]
        TR_table[i] = [row[0],row[1],row[4],row[7],row[10],row[13]]

    return TR_table



def Get_TransitionRates_GndTruth_Data(atom,gnd_truth_url):

    #Start by fetching the ground truth tables a.k.a tables from version 2
    TR_table_gnd_truth = fetch_TransitionRates_tables(atom,gnd_truth_url)

    #Buttons list (There are some unwanted rows such as the column headers)
    #Unwanted rows are ignored
    GndTruth_btns_list = TR_table_gnd_truth[0]
    GndTruth_btns_list = GndTruth_btns_list[2:]

    #Unwanted rows ignored for Radiative liftimes tables
    GndTruth_radiativelifetimes_data = TR_table_gnd_truth[1]
    GndTruth_radiativelifetimes_data = GndTruth_radiativelifetimes_data[1:]

    #Unwanted rows ignored for the Transition rates tables
    GndTruth_TR_data = TR_table_gnd_truth[2]
    
    #Preprocessing required for the transitions rates tables
    GndTruth_TR_data = utils.preprocess(GndTruth_TR_data,data_type)
    GndTruth_TR_data = GndTruth_TR_data[1:]
    
    GndTruth_TR_data = getRelevant_TR_data(GndTruth_TR_data)

    states_list = []

    #Removing unwanted spaces from button lists and gathering all the buttons
    for btn_row in GndTruth_btns_list:
        if(len(btn_row)>1):
            for btn in btn_row:
                if((btn != '') and (btn not in states_list)):
                    states_list.append(btn.replace(" ", ""))

    #Remove unwanted spaces within the state values in radiative liftimes data
    #i.e. e.g. '3s 1/2' is changed to '3s1/2'
    for i in range(0,len(GndTruth_radiativelifetimes_data)):
        rl_row = GndTruth_radiativelifetimes_data[i]
        rl_row[0] =rl_row[0].replace(" ", "")
        GndTruth_radiativelifetimes_data[i] = rl_row
        
    #Populate a dictionary of the ground truth (version 2) data
    # key: state, value: [radiative lifetimes data, transiton rates data]

    # First populate the dictionary with the radiative lifetimes data
    actual_data = {}
    for state in states_list:
        temp_list = []
        for rl_row in GndTruth_radiativelifetimes_data:
            if (state == rl_row[0]):
                temp_list.append(rl_row)

        for TR_row in GndTruth_TR_data:
            if(state == TR_row[0]):
                temp_list.append(TR_row)
        
        actual_data[state] = temp_list

    return actual_data