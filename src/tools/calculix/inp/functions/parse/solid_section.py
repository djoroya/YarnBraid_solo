from tools.calculix.inp.MaterialCard import MaterialCard 
from tools.calculix.inp.SolidSectionCard import SolidSectionCard
from tools.calculix.inp.ElsetCard import ElsetCard
from tools.calculix.inp.ElsetofElsetCard import ElsetofElsetCard

def parse_solid_section(name,new_cards,verbose=False):

    printw = lambda x: print(x) if verbose else None
    opt = name.replace("*SOLIDSECTION,","").split(",")
    opt = [i.split("=") for i in opt]
    opt = {i[0]:i[1] for i in opt}

    elset = [ icard for icard in new_cards
                if (isinstance(icard,ElsetCard) or isinstance(icard,ElsetofElsetCard))
                if icard.name == opt["ELSET"]]

    material = [ icard for icard in new_cards
                if isinstance(icard,MaterialCard)
                if icard.name == opt["MATERIAL"]]

    if len(elset) == 0:
        printw("No existe el elset: "+opt["ELSET"])
        printw("*SOLID SECTION")

        return None
    if len(elset) > 1:
        printw("Existe mas de un elset: "+opt["ELSET"])
        printw("*SOLID SECTION")

        return None
    if len(material) == 0:
        printw("No existe el material: "+opt["MATERIAL"])
        printw("*SOLID SECTION")

        return None
    if len(material) > 1:
        printw("Existe mas de un material: "+opt["MATERIAL"])
        printw("*SOLID SECTION")

        return None

    elset  = elset[0]
    material = material[0]

    new_card = SolidSectionCard(elset,material)

    return new_card