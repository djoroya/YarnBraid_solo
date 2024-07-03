from tools.calculix.inp.Card import Card

class ElasticCard (Card):
    def __init__(self, name, E,nu):
        super().__init__(name, name)

        self.E  = E
        self.nu = nu
        self.type = '*ELASTIC'

    def print(self):

        return "*ELASTIC\n{},{}\n".format(self.E,self.nu)

class DensityCard (Card):
    def __init__(self, name, rho):
        super().__init__(name, name)

        self.rho  = rho
        self.type = '*DENSITY'

    def print(self):
        return "*DENSITY\n{}\n".format(self.rho)

class MaterialCard (Card):
    def __init__(self, name, cards):
        super().__init__(name, name)
        self.type = "*MATERIAL"

        self.cards = cards

    def print(self):
        
        lines = "*MATERIAL, NAME={}\n".format(self.name)
        for card in self.cards:
            lines = lines + card.print()
        return lines