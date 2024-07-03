from tools.calculix.inp.Card import Card
from tools.calculix.inp.ElsetCard import ElsetCard
from tools.calculix.inp.MaterialCard import MaterialCard
from tools.calculix.inp.ElsetofElsetCard import ElsetofElsetCard
class SolidSectionCard (Card):
    def __init__(self, elset, material):
        name = "SOLID_SECTION"
        super().__init__(name, name)

        if not (isinstance(elset, ElsetCard) or isinstance(elset, ElsetofElsetCard)):
            raise Exception("elset must be an ElsetCard or ElsetofElsetCard")
        if not isinstance(material, MaterialCard):
            raise Exception("material must be a MaterialCard")
        
        self.elset     = elset
        self.material  = material
        self.type = '*SOLIDSECTION'

    def print(self):
        # print the nodes but only in row of 10
        return '*SOLID SECTION , ELSET=' + self.elset.name_up + ', MATERIAL=' + self.material.name_up
