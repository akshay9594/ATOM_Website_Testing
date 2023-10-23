
import webscrapper

def split_list(input_list, split_val):
    size = len(input_list)
    idx_list = [idx + 1 for idx, val in
            enumerate(input_list) if val == split_val]

 
    res = [input_list[i: j] for i, j in
       zip([0] + idx_list, idx_list +
           ([size] if idx_list[-1] != size else []))]
    
    return res

def preprocess(data:list,data_type:str):
    if(data_type == 'TransitionRates'):
        input_list = data[0]
        split_result = split_list(input_list,'DOI 2')
        data.remove(input_list)
        data.insert(0,split_result[1])
        data.insert(0,split_result[0])
        return data
    
    if(data_type == 'MatrixElements'):
        input_list = data[1][0]
        split_DOI = split_list(input_list,'DOI 2')
        data[1].remove(input_list)
        data[1].insert(0,split_DOI[1])
        data[1].insert(0,split_DOI[0])

        split_Initial = split_list(input_list,'Initial')
        Final_state_lst = split_Initial[0]
        Final_state_lst.pop()
        data[0].append(Final_state_lst)
   
        return data
    


def get_gnd_truth_tables(atom,url,data_type,ext):
    # defining the html contents of a URL.
    html_file = webscrapper.static_page_scrapper(atom,url,ext,data_type)

    p = webscrapper.get_html_feed(html_file)
    
    # Now finally obtaining the data of
    # the table required

    if (ext == 'version1'):
        if (data_type=='Hyperfine' or data_type == 'Nuclear'):
            return p.tables[0],p.tables[1]
        elif (data_type == 'TransitionRates'):
            return p.tables[0],p.tables[1],p.tables[2]
        elif (data_type == 'MatrixElements'):
            return p.tables[0],p.tables[1],p.tables[2]
        
    elif (ext == 'version2'):
        if (data_type=='Hyperfine' or data_type == 'Nuclear'or data_type == 'Energies'):
            return p.tables[0]
        elif (data_type == 'TransitionRates'):
            return p.tables[0],p.tables[1],p.tables[2]
        elif (data_type == 'MatrixElements'):
            return p.tables[0],p.tables[1],p.tables[2]
        
