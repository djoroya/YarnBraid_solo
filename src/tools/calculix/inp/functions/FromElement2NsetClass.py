import numpy as np
from tools.calculix.inp.NsetCard import NsetCard

def FromElement2NsetClass(self,element,name):

    id_values_list = element.GetUniqueNodes(self.nodes).index.values

    nset = NsetCard(name, id_values_list)

    self.cards = np.append(self.cards,nset)
    self.nsets = [card for card in self.cards 
                    if card.type == '*NSET']

    # add to cards and nsets
    return nset