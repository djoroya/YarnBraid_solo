import numpy as np
from tools.calculix.inp.NsetCard import NsetCard
def parse_nset(icard):
    id_nodes = icard[1:]
    # remove the \n
    id_nodes = [i.replace('\n','') for i in id_nodes]
    # join the list
    id_nodes = ''.join(id_nodes).split(',')
    # remove empty elements
    id_nodes = [i for i in id_nodes 
            if i != '']                    
    # to int 
    id_nodes = np.array(id_nodes,dtype=int)
    name = icard[0].replace(" ","").split("=")
    name = name[1]
    new_card = NsetCard(name,id_nodes)
    return new_card