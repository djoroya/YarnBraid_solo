from tools.calculix.inp.Card import Card


class ElsetofElsetCard (Card):
    def __init__(self, name, id_elements):
        super().__init__(name, id_elements)

        self.id_elements = id_elements
        self.type = '*ELSETOFELSET'

    def print(self):
        # print the nodes but only in row of 10
        line = ''
        for i, element in enumerate(self.id_elements):
            line += str(element) + ','
            if i % 10 == 0 and i != 0:
                line += '\n'
        line = line[:-1]
        return '*ELSET, ELSET=' + self.name_up + '\n' + line 
