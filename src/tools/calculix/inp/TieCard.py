from tools.calculix.inp.Card import Card


class TieCard (Card):
    def __init__(self, name, slave, master):
        super().__init__(name, name)

        self.master = master
        self.slave  = slave
        self.type = '*TIE'

    def print(self):
        # print the nodes but only in row of 10
        return self.type    + ', NAME=' +\
               self.name_up + ',position tolerance=0.1\n' +\
               self.slave.name_up + ', ' + self.master.name_up

    def restart_index_element(self, id_elements):
        self.id_elements = self.id_elements + id_elements

        return self
