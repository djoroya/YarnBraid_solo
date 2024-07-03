import numpy as np
from tools.calculix.inp.NsetCard import NsetCard
def FromElement2Nset(self,index_el,name=None):

    id_values_list = []
    for i in index_el:
        el = self.elements[i].GetUniqueNodes(self.nodes).index.values
        id_values_list.append(el)
    id_values_list = np.concatenate(id_values_list)
    if name is None:
        name = self.elements[i].options["ELSET"]

    nset = NsetCard(name, id_values_list)

    self.cards = np.append(self.cards,nset)
    self.nsets = [card for card in self.cards if card.type == '*NSET']

    # add to cards and nsets
    return nset