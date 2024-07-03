from tools.calculix.inp.Card import Card


class SurfaceNodeCard (Card):
    def __init__(self, name, nset):
        super().__init__(name, nset)

        self.nset = nset
        self.type = '*SURFACE'

    def print(self):
        # print the nodes but only in row of 10
        return self.type    + ', NAME=' +\
               self.name_up + ',TYPE=NODE\n' +\
               self.nset.name 

    def restart_index_element(self, id_elements):
        self.id_elements = self.id_elements + id_elements

        return self
