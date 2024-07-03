import numpy as np
from tools.calculix.inp.NodeCard               import NodeCard
from tools.calculix.inp.ElementCard            import ElementCard
from tools.calculix.inp.Card                   import Card

from tools.calculix.inp.functions.parse.surface import parse_surface
from tools.calculix.inp.functions.parse.contact import parse_contact
from tools.calculix.inp.functions.parse.tie     import parse_tie
from tools.calculix.inp.functions.parse.nset    import parse_nset
from tools.calculix.inp.functions.parse.surface_interaction import parse_surface_interaction
from tools.calculix.inp.functions.parse.elset         import parse_elset
from tools.calculix.inp.functions.parse.material      import parse_material
from tools.calculix.inp.functions.parse.solid_section import parse_solid_section
from tools.calculix.inp.functions.parse.step import parse_step

def init(self, file_name,warning=True):

        printw = lambda x: print(x) if warning else None

        self.file_name = file_name
        #open 
        lines = open(file_name).readlines()
        # upper case
        lines = [line.upper() for line in lines]
        # remove empty spaces in the start of the line
        lines = [line.lstrip() for line in lines]
        # remove lines since *STEP or *step 
        id_step = [i for i, line in enumerate(lines) 
                   if line.startswith('*STEP')]
        if len(id_step) > 0:
            step_lines = lines[id_step[0]:]
            lines = lines[:id_step[0]]
        else:
            step_lines = []
        #step line
        
        # remove lines starting with '**'
        lines = [line for line in lines if not line.startswith('**')]
        # remove empty lines
        id_empty = [i for i, line in enumerate(lines) if line == '\n']
        # write the lines without empty lines
        lines = [line for i, line in enumerate(lines) if i not in id_empty]
        # open the file and write the lines in try.inp
        # search the lines start with '*' take the index
        #index = [lines.index(line) for line in lines if line.startswith('*')]
        index = [i for i, line in enumerate(lines) if line.startswith('*')]
        # add the last line
        index.append(len(lines))
        # split the lines into cards
        cards = [lines[index[i]:index[i+1]] for i in range(len(index)-1)]
        # the fisrt card is the header and the next lines are the content
        # remove empty cards
        cards = [card for card in cards if len(card) > 0]
        self.contents = cards

        new_cards = []
        for index,icard in enumerate(cards):

            if len(icard) == 0:
                printw("Card vacia")
                continue 
            if not icard[0].startswith('*'):
                if warning:
                    KeyError('Card name is not correct, The card name must start with *')

            name    = icard[0].upper().replace(" ","").replace("\n","")
            content = icard[1:]
            # remove empty lines
            content = [line for line in content if line != '']
            try:
                if name.startswith('*NODE'):
                    new_card = NodeCard(name, content)
                elif name.startswith("*ELEMENT"):
                    new_card = ElementCard(name,content)
                    if new_card.dimension == -1:
                        printw("Element type not implemented")
                        continue
                elif name.startswith("*NSET"):
                    new_card = parse_nset(icard)
                elif name.startswith("*ELSET"):
                    new_card = parse_elset(content,name)
                elif name.startswith("*SURFACE,"):
                        new_card = parse_surface(name,content,new_cards,warning)
                elif name.startswith("*SURFACEINTERACTION"):
                    new_card = parse_surface_interaction(name,cards,index,warning)
                elif name.startswith("*SURFACEBEHAVIOR"):
                    continue
                elif name.startswith("*CONTACTPAIR"):
                    new_card = parse_contact(name,content,new_cards,warning)
                elif name.startswith("*TIE"):
                    new_card = parse_tie(name,content,new_cards,warning)
                elif name.startswith("*EQUATION"):
                    continue
                elif name.startswith("*MATERIAL"):
                    new_card = parse_material(name,content,cards,index)
                elif name.startswith("*SOLIDSECTION"):
                    new_card = parse_solid_section(name,new_cards,warning)
                else:
                    new_card = Card(name, content)
                if new_card is not None:
                    new_cards.append(new_card)
            except Exception as e:
                printw("Error en la linea: "+name)
        if len(step_lines) > 0:
            step_cards = parse_step(step_lines,new_cards)
            new_cards.extend(step_cards)
        
        new_cards = np.array(new_cards)
        self.cards = new_cards

        self.frd = None

        self = self.reset_cards()