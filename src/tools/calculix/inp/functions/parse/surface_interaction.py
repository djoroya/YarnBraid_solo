from tools.calculix.inp.SurfaceInteractionCard import SurfaceInteractionCard

def parse_surface_interaction(name,cards,index,verbose=False):
   
    printw = lambda x: print(x) if verbose else None    
    next_card = cards[index+1]
    next_name = next_card[0].upper().replace(" ","").replace("\n","")
    if not next_name.startswith("*SURFACEBEHAVIOR,"):
        printw("* SURFACE INTERACTION must be followed by *SURFACEBEHAVIOR")
        return None
    next_name = next_name.replace("*SURFACEBEHAVIOR,,","")
    opt_surf = next_name.split("=")
    type = opt_surf[1]
    name = name.replace("*SURFACEINTERACTION,","")
    name = name.split("=")
    name = name[1]
    new_card = SurfaceInteractionCard(name,type)
    return new_card