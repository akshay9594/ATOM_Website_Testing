

def element_data(atom,req_data):
    switcher = {
        "Li": 1,"Cs": 7,
        "Na": 1,
        "K": 1,"Ce": 10,
        "Rb": 1,"Pr": 11,
        "Cs": [1,7],"Nd":[12,13,14],
        "Fr": 1,"Sm":[14,15,16],
        "Be": 2,"Eu": 15,
        "Mg": 2,"Cf": [16,18],
        "Ca": 2,
        "Sr": [1,2],
        "Ba": [2,8],
        "Ra": 2,

    }
 
    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument

    if(req_data == 'element list'):
        return list(switcher.keys())
    else:
        return switcher.get(atom, "nothing")

    