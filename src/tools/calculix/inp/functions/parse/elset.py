from tools.calculix.inp.ElsetCard import ElsetCard
from tools.calculix.inp.ElsetofElsetCard import ElsetofElsetCard
import numpy as np

def parse_elset(content,name):
    c = "".join(content)
    c = c.replace('\n','')
    c = c.split(',')
    if c[-1] == '':
        c = c[:-1]
    name = name.replace("\n","").split("ELSET=")[-1]

    try:
        c = np.array(c,dtype=int)
        new_card = ElsetCard(name,c)
    except:
        new_card = ElsetofElsetCard(name,c)

    return new_card