
import os
import csv


#Preprocessing data to remove white space
def preprocess(data:list):
    for data_list in data:
        for i in range(0,len(data_list)):
            data_list[i] = data_list[i].replace(" ", "")
    return data

def fetchPolarizabilityData(path_to_data):

    StaticPol_data = ''
    Pol_States_data = {}

    #Scan the Data directory to get all the files
    obj = os.scandir(path_to_data)
    
    static_pol_file = ''
    list_pol_states_files = []

    #Go through all the files and separate out the Static Pol file
    # and the Pol files for states. Get the states Pol files into a list
    for entry in obj:
        if entry.is_file():
            file_name = entry.name
            if('StaticPol' in file_name):
                static_pol_file = file_name
            elif('.DS_Store' not in file_name):
                list_pol_states_files.append(file_name)

    path_to_StaticPol_file = path_to_data + '/' + static_pol_file

    #Read the Static Pol data
    with open(path_to_StaticPol_file, 'r') as file:
        StaticPol_data = list(csv.reader(file, delimiter=","))

    #Preprocess the Static Pol data to remove white spaces
    StaticPol_data = preprocess(StaticPol_data)

    #Read the States Pol data into a dictionary. The states form the keys.
    for state_file_name in list_pol_states_files:
        path_to_file = path_to_data + '/' + state_file_name
        with open(path_to_file, 'r') as file:
            first_line = file.readline()
            state = first_line.split(",")[1]
            Pol_data = list(csv.reader(file, delimiter=","))
            #Preprocess the data to remove white spaces
            Pol_data = preprocess(Pol_data)
            Pol_States_data[state] = Pol_data

    return StaticPol_data, Pol_States_data