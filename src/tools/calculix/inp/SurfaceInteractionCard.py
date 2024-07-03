from tools.calculix.inp.Card import Card


class SurfaceInteractionCard (Card):
    def __init__(self, name, type):
        super().__init__(name, name)
        self.type = "*SURFACEINTERACTION"
        self.interaction = type
    def print(self):
        return '*SURFACE INTERACTION, NAME=' + self.name_up  + "\n*SURFACE BEHAVIOR, PRESSURE-OVERCLOSURE=HARD\n"
