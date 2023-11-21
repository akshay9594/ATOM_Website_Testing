



import sys,os,re

sys.path.append(os.getcwd()+'/fetch_Gnd_TRuth_Data')

import utils

data_type = 'Atomic'


def fetch_Atomic_tables(atom,url):

    gndTruth_file = atom + 'hci.html'
    url = url + gndTruth_file
    Energies_Table,TREnergies_Table = utils.get_gnd_truth_tables(atom,url,data_type,'version2')

    return Energies_Table,TREnergies_Table

def Get_Atomic_data(atom,gnd_truth_url):

    gndTruth_Energy_Table,gndTruth_TREnergy_Table = fetch_Atomic_tables(atom,gnd_truth_url)

    if(gndTruth_Energy_Table == [] or gndTruth_TREnergy_Table == []):
        return [],[]
    else:
        gndTruth_Energy_Table = gndTruth_Energy_Table[2:]
        exclude = '\\'
        for row in gndTruth_Energy_Table:
            for i in range(0,len(row)):
                #row[i] = row[i].replace("$","").replace("_","").replace("{","").replace("}","")

                row[i] = re.sub('[{$times_}]', '', row[i])

                row[i] = ''.join(ch for ch in row[i] if ch not in exclude)

        gndTruth_TREnergy_Table = gndTruth_TREnergy_Table[2:]

        for row in gndTruth_TREnergy_Table:
            for i in range(0,len(row)):
                #row[i] = row[i].replace("$","").replace("_","").replace("{","").replace("}","")

                row[i] = re.sub('[{$times_}]', '', row[i])
                row[i] = ''.join(ch for ch in row[i] if ch not in exclude)

        return gndTruth_Energy_Table, gndTruth_TREnergy_Table