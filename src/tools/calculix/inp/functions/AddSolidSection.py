import numpy as np
from tools.calculix.inp.SolidSectionCard import SolidSectionCard

def AddSolidSection(self,elset,material):
        # master must be type SurfaceCard

    elset = self.select(elset,"elset")
    material  = self.select(material,"material")

    ssec = SolidSectionCard(elset,material)
    self.cards = np.append(self.cards,ssec)
    self.SolidSections = [card for card in self.cards if card.type == '*SOLIDSECTION']
    
    return ssec