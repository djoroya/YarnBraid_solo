import numpy as np
def addStep(inp_files,contacts,file,params):
    names = [ element.options["ELSET"] for element in inp_files[0].elements]
    lines = "*Elset, Elset = ALL\n"
    for j,name in enumerate(names):
        if j == len(names)-1:
            lines = lines + name + "\n"
        else:
            lines = lines + name + ",\n"

    # ==============================================================================

    # all index nodes in NSET named ALL
    nodes_id = inp_files[0].nodes.df.index.values
    lines = lines + "*Nset, Nset = ALL_NODES\n"
    # write the nodes in the NSET ( every 10 values add a new line)
    for i in range(len(nodes_id)):
        if i % 10 == 0:
            lines = lines + str(nodes_id[i]) + ",\n"
        else:
            lines = lines + str(nodes_id[i]) + ", "
    lines = lines[:-1]
    # 
    # 
    list_str = ["_CENTRAL",""]
    for ils in list_str:
    # 
        BOT_NAME_NSET = [ inset.name for inset in inp_files[0].nsets 
                        if "BOT"+ils in inset.name ]
        TOP_NAME_NSET = [ inset.name for inset in inp_files[0].nsets 
                        if "TOP"+ils in inset.name ]

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

    ##

    # ==============================================================================
    #  MATERIAL
    # ==============================================================================
    young    = 2960
    poisson  = 0.0
    pressure = params["pressure"]

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
""".format(young,poisson)
    
    # ==============================================================================
    #  SURFACE
    # ==============================================================================
    lines = lines + """**
** Surface interactions ++++++++++++++++++++++++++++++++++++
**
*Surface interaction, Name=SURFACE_INTERACTION_1
"""
    
    if params["surface_behavior"]["type"] == "hard":
        lines = lines + "*Surface behavior, Pressure-overclosure=Hard"
    elif params["surface_behavior"]["type"] == "exponential":
        lines = lines + "*Surface behavior, Pressure-overclosure=EXPONENTIAL\n{},{}".format(params["surface_behavior"]["dist"],params["surface_behavior"]["pressure"])
    
    lines = lines + """\n
**
** Contact pairs +++++++++++++++++++++++++++++++++++++++++++
**
"""

    # cada grupo de 4 se tocas entre si
    iter = 0
    for i in range(len(contacts)):

        iter = iter + 1
        lines = lines + "*Contact pair, Interaction=SURFACE_INTERACTION_1, Type=Surface to surface\n"
        slave  = contacts[i][0]
        master = contacts[i][1]
        if slave == 1 and master == 1:
            lines = lines + "SURFACE_{}, SURFACE_{}\n**\n".format(slave, master)
        elif slave == 1 and master != 1:
            lines = lines + "SURFACE_{}, P{}_SURFACE_{}\n**\n".format(slave,master,master)
        elif slave != 1 and master == 1:
            lines = lines + "P{}_SURFACE_{}, SURFACE_{}\n**\n".format(slave,slave,master)
        else:
            lines = lines + "P{}_SURFACE_{}, P{}_SURFACE_{}\n**\n".format(slave,slave,master,master)

    
    def create_Step(pressure):
        step_lines = "*Step\n*Static\n*Boundary, op=New\n"
        for i in range(len(inp_files)):
            if i == 0:
                line = "*Boundary\nESQUELETO_"+str(i+1)+", 1, 6, 0\n"
            else:
                line = "*Boundary\nP"+str(i+1)+"_ESQUELETO_"+str(i+1)+", 1, 6, 0\n"
            step_lines = step_lines + line

        step_lines = step_lines + "*Cload, op=New\n"

        for i in range(len(inp_files)):
            step_lines = step_lines + "*Dload\n"
            if i == 0:
                prefix = ""
            else:
                prefix = "P"+str(i+1)+"_"
            for j in range(4):
                line = prefix+"ELSET_SURFACE_SURFACE_" + \
                    str(i+1)+"_"+str(j+1)+", P"+str(j+1)+", -{}\n".format(pressure)
                step_lines = step_lines + line

        line = """**
*Node file
RF, U
*El file
S, E
*Contact file
CDIS, CSTR, PCON
*NODE PRINT,NSET=ALL_NODES
U
*EL PRINT, ELSET=ALL
EVOL
**
*End step
"""

        step_lines = step_lines + line
        return step_lines


    nsteps = params["nsteps"]
    p_span = np.linspace(0,pressure,nsteps+1)
    p_span = p_span[1:]
    for i in range(nsteps):
        lines = lines + create_Step(p_span[i])
    # add to the end on prueba.inp
    with open(file, "a") as f:
        f.write(lines)