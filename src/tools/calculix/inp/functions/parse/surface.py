from tools.calculix.inp.SurfaceCard import SurfaceCard
from tools.calculix.inp.SurfaceNode import SurfaceNodeCard
from tools.calculix.inp.NsetCard import NsetCard
from tools.calculix.inp.ElsetCard import ElsetCard


def parse_surface(name,content,new_cards,verbose=False):

    printw = lambda x: print(x) if verbose else None

    name_surf = name.replace("*SURFACE,","")
    opt_surf = name_surf.split(",")
    opt_surf = [i.split("=") for i in opt_surf]
    opt_surf = {i[0]:i[1] for i in opt_surf}

    name_surf = opt_surf["NAME"]
    ncontent = content[0].replace("\n","").replace(" ","")

    if opt_surf["TYPE"] != "ELEMENT":
        
        nset = [ icard for icard in new_cards
                    if isinstance(icard,NsetCard)
                    if icard.name == ncontent]
        if len(nset) == 0:
            printw("No existe nset: "+ncontent)
            return None
        if len(nset) > 1:
            printw("Existe mas de un nset: "+ncontent)
            return None
        nset = nset[0]
        new_card = SurfaceNodeCard(name_surf,nset)

    else:
        csurf = [i.replace("\n","") for i in content]
        csurf = [i.split(",") for i in csurf]
        csurf = {i[1]:i[0] for i in csurf}

        surf_elset  = []
        for i in range(1,5):
            if "S"+str(i) not in csurf.keys():
                string ="_".join(csurf[list(csurf.keys())[0]].split("_")[:-1])
                string = string  + "_"+str(i)
                csurf["S"+str(i)] = string
            surfaces_el = [ icard for icard in new_cards 
                    if isinstance(icard,ElsetCard)
                    if icard.name == csurf["S"+str(i)]]
            if len(surfaces_el) == 0:
                printw("No existe elset: "+csurf["S"+str(i)])
                continue
            if len(surfaces_el) > 1:
                printw("Existe mas de un elset: "+csurf["S"+str(i)])
                continue
            surf_elset.append(surfaces_el[0])
        new_card = SurfaceCard(name_surf,surf_elset)
    
    return new_card