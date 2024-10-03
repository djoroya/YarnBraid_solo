import numpy as np
def addStep(inp_files,contacts,file,params):
    names = [ element.options["ELSET"] for element in inp_files.elements]
    lines = "*Elset, Elset = ALL\n"
    for j,name in enumerate(names):
        if j == len(names)-1:
            lines = lines + name + "\n"
        else:
            lines = lines + name + ",\n"

    # ==============================================================================

    # all index nodes in NSET named ALL
    nodes_id = inp_files.nodes.df.index.values
    lines = lines + "*Nset, Nset = ALL_NODES\n"
    # write the nodes in the NSET ( every 10 values add a new line)
    for i in range(len(nodes_id)):
        if i % 10 == 0:
            lines = lines + str(nodes_id[i]) + ",\n"
        else:
            lines = lines + str(nodes_id[i]) + ", "
    lines = lines[:-1]
    # ==============================================================================
    list_str = ["_CENTRAL",""]
    for ils in list_str:
    # 
        BOT_NAME_NSET = [ inset.name for inset in inp_files.nsets 
                        if "BOT"+ils in inset.name 
                        if "CIRC" not in inset.name
                        if "_REP" not in inset.name ]
                          
                        
        TOP_NAME_NSET = [ inset.name for inset in inp_files.nsets 
                        if "TOP"+ils in inset.name 
                        if "CIRC" not in inset.name
                        if "_REP" not in inset.name ]

        line = "\n*Nset, Nset = BOT"+ils+"\n"
        for i in range(len(BOT_NAME_NSET)):
            if i == len(BOT_NAME_NSET)-1:
                line = line + BOT_NAME_NSET[i] + "\n"
            else:
                line = line + BOT_NAME_NSET[i] + ",\n"

        line = line + "*Nset, Nset = TOP"+ils+"\n"
        for i in range(len(TOP_NAME_NSET)):
            if i == len(TOP_NAME_NSET)-1:
                line = line + TOP_NAME_NSET[i] + "\n"
            else:
                line = line + TOP_NAME_NSET[i] + ",\n"
                
        lines = lines + line
    # ==============================================================================
    # only braid yarns
    for ils in list_str:
    # 
        BOT_NAME_NSET = [ inset.name for inset in inp_files.nsets 
                        if "CIRC" not in inset.name
                        if "_REP" not in inset.name
                        if "BOT"+ils in inset.name ]
        TOP_NAME_NSET = [ inset.name for inset in inp_files.nsets
                        if "CIRC" not in inset.name
                        if "_REP" not in inset.name
                        if "TOP"+ils in inset.name ] 
        
        BOT_NAME_NSET = BOT_NAME_NSET[:64]
        TOP_NAME_NSET = TOP_NAME_NSET[:64]

        line = "\n*Nset, Nset = BOT_BRAID"+ils+"\n"
        for i in range(len(BOT_NAME_NSET)):
            if i == len(BOT_NAME_NSET)-1:
                line = line + BOT_NAME_NSET[i] + "\n"
            else:
                line = line + BOT_NAME_NSET[i] + ",\n"

        line = line + "*Nset, Nset = TOP_BRAID"+ils+"\n"
        for i in range(len(TOP_NAME_NSET)):
            if i == len(TOP_NAME_NSET)-1:
                line = line + TOP_NAME_NSET[i] + "\n"
            else:
                line = line + TOP_NAME_NSET[i] + ",\n"
                
        lines = lines + line
    # ==============================================================================
    young    = 2960
    poisson  = 0.0
    pressure = params["pressure"]

    if params["surface_behavior"]["type"] == "hard":
        surface_interaction = "*Surface behavior, Pressure-overclosure=Hard"
    elif params["surface_behavior"]["type"] == "linear":
        surface_interaction = "*Surface behavior, Pressure-overclosure=linear\n{}".format(params["factor_contact"]*young)
    elif params["surface_behavior"]["type"] == "exponential":
        surface_interaction = "*Surface behavior, Pressure-overclosure=exponential\n{}".format(params["factor_contact"]*young)
    else:
        raise ValueError("type_contact must be hard or linear")

    lines = lines + """
**
*Material, Name=PET
*Density
1.42E-09
*Elastic
{},{}
*Expansion, Zero=20
6.5E-05
*Conductivity
0.261
*Specific heat
1140000000
**
*Solid section, Elset=ALL, Material=PET
**
** Surface interactions ++++++++++++++++++++++++++++++++++++
**
*Surface interaction, Name=SURFACE_INTERACTION_1
{}
**
** Contact pairs +++++++++++++++++++++++++++++++++++++++++++
**
    """.format(young,poisson,surface_interaction)

    # cada grupo de 4 se tocas entre si
    iter = 0
    for i in range(len(contacts)):

        iter = iter + 1
        lines = lines + "*Contact pair, Interaction=SURFACE_INTERACTION_1, Type=Surface to surface\n"
        lines = lines + \
            "SURFACE_{}, SURFACE_{}\n**\n".format(
                contacts[i][0], contacts[i][1])

    if params["nlgeom"]:
        nlgemo=",nlgeom"
    else:
        nlgemo=""

    Nhilos = len(inp_files.elements)
    def gen_step(pressure):
        step_lines = """**
**
*Step{}
*Static
*Boundary, op=New
""".format(nlgemo)
            


        for i in range(Nhilos):
            prefix =  "P{}_".format(i+1) if i != 0 else ""
            line = "*Boundary\n"+prefix+"ESQUELETO_"+str(i+1)+", 1, 6, 0\n"
            step_lines = step_lines + line

        step_lines = step_lines + "*Cload, op=New\n"

        for i in range(Nhilos):
            step_lines = step_lines + "*Dload\n"
            for j in range(4):
                line = "ELSET_SURFACE_SURFACE_" + \
                    str(i+1)+"_"+str(j+1)+", P"+str(j+1)+", -{}\n".format(pressure)
                step_lines = step_lines + line

        step_lines =step_lines+ """**
*Node file
RF, U
*El file
S, E
*Contact file
CDIS, CSTR, PCON
*NODE PRINT,NSET=ALL_NODES
U
**
*End step 
"""
        return step_lines
    
    step_lines = ""    
    nsteps = params["nsteps"]
    p_space = np.linspace(0,pressure,nsteps+1)
    p_space[0] = 0.25*p_space[1]
    for i in range(nsteps+1):
        step_lines = step_lines + gen_step(p_space[i])
    lines = lines + step_lines

    # add to the end on prueba.inp
    with open(file, "a") as f:
        f.write(lines)