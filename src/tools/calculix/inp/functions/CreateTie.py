from tools.calculix.inp.TieCard import TieCard
import numpy as np

def CreateTie(self,name,slave,master,type="surface"):
    # master must be type SurfaceCard
    if type not in ["surface","nset"]:
        raise Exception("type must be surface or nset")

    master = self.select(master,"surface")
    slave  = self.select(slave,type)

    tie = TieCard(name,slave,master)
    self.cards = np.append(self.cards,tie)
    self.ties = [card for card in self.cards if card.type == '*TIE']
    
    return tie