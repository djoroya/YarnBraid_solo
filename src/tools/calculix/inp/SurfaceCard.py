from tools.calculix.inp.Card import Card


class SurfaceCard (Card):
    def __init__(self, name, elsets):
        super().__init__(name, elsets)

        self.elsets = elsets
        self.type = '*SURFACE'

    def print(self):
        line = ''
        for i, elset in enumerate(self.elsets):
            if len(elset.id_elements) == 0:
                continue
            # last 
            line += str(elset.name) + ',S' + str(i+1) + '\n' 
        line = line[:-1]
        return self.type + ', NAME=' + self.name_up  +",TYPE=ELEMENT"+ '\n' + line 
