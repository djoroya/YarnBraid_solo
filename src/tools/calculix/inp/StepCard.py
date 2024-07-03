from tools.calculix.inp.Card import Card

class StepCard (Card):
    def __init__(self, cards):
        name = "STEP"
        super().__init__(name, name)
        self.type = "*STEP"

        self.cards = cards

    def print(self):
        
        lines = "*STEP\n"
        for card in self.cards:
            lines = lines + card.print()
        return lines