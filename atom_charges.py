

def atom_charge(atom):
    switcher = {
        "Li": 1,"Cs": 7,
        "Na": 1,"Ba": 8,
        "K": 1,"Ce": 10,
        "Rb": 1,"Pr": 11,
        "Cs": 1,"Nd":[12,13,14],
        "Fr": 1,"Sm":[14,15,16],
        "Be": 2,"Eu": 15,
        "Mg": 2,"Cf": [16,18],
        "Ca": 2,
        "Sr": 2,
        "Ba": 2,
        "Ra": 2,

    }
 
    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return switcher.get(atom, "nothing")
    