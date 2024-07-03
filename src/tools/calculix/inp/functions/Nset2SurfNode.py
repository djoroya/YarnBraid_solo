import numpy as np
from tools.calculix.inp.SurfaceNode            import SurfaceNodeCard

def Nset2SurfNode(self,id_values_list,name=None):
        
    nset = SurfaceNodeCard(name, id_values_list)

    self.cards = np.append(self.cards,nset)
    self.surfaces = [card for card in self.cards 
                        if card.type == '*SURFACE']

    # add to cards and nsets
    return nset