import os
import numpy as np



def addStep(ls,nsets,params,displ):
 
    nonlinear = params["nonlinear"]
    cylindrical = params["cylindrical"]
    # ==============================================================================
    ls.wt("**"                         )
    ls.wt("*Step, Nlgeom"  if nonlinear else "*Step" )           
    ls.wt("*Static"                        )
    ls.wt("*Output, Frequency=1"           )
    ls.wt("*RESTART, WRITE, frequency=1"   )
    ls.wt("*Boundary, op=New"               )

    # ==============================================================================
    type_bc = params["type_bc"]
    only_braid = params["only_braid"]
    sufix = "_BRAID" if only_braid else ""
    # *** Boundary conditions ***
    # 1: BOT is fixed and TOP is displaced
    if not cylindrical:
        if type_bc == 1:
        # BOT is fixed and TOP is displaced
        # TOP is displaced in z direction and x and y are fixed
        # ==============================================================================
                ls.wt("*Boundary\nBOT"+sufix+", 1, 6, 0" )
                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ) )

        # 2: BOT is fixed and TOP is displaced
        # BOT is fixed and TOP is displaced
        # TOP is displaced in z direction and x and y are fixed
        # 3: BOT is fixed and TOP is displaced
        # BOT is fixed and TOP is displaced
        # ==============================================================================
        elif type_bc == 2 or type_bc == 3:

                bot_names = [ ikey 
                                for ikey in nsets.keys() 
                                if "BOT" in ikey ]
                
                nbot = len(bot_names)

                ls.wt("*Boundary\nBOT"+sufix+", 1, 6, 0" )
                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ) )
                
                nfixed = params["nfixed"]
                arr_nbot = np.arange(0,nbot,int(nbot/nfixed))

                id_node_fcn = lambda x: nsets[bot_names[x]][0]
                ls.wt("*Boundary\n{}, 1, 3, 0".format(id_node_fcn(0)))

                if type_bc == 2:
                        # 3 degrees of freedom are fixed
                        for i in arr_nbot[1:]:
                                ls.wt("*Boundary\n{}, 1, 3, 0".format(id_node_fcn(i)))
                elif type_bc == 3:
                        # 1 degree of freedom are fixed and z is fixed
                        for i in arr_nbot[1:]:
                                ls.wt("*Boundary\n{}, 2, 2, 0".format(id_node_fcn(i)))
        # 4: BOT is fixed and TOP is displaced
        # BOT is fixed and TOP is displaced
        # ==============================================================================
        elif type_bc == 4:
                # Tiramos de los dos extremos sin fijar x ni y
                ls.wt("*Boundary\nBOT"+sufix+", 3, 3, {}".format(displ/2) )
                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ/2) )
        # 5: BOT is fixed and TOP is displaced
        # BOT is fixed and TOP is displaced
        # ==============================================================================
        elif type_bc == 5:
                # Tiramos de los dos extremos fixando x e y
                ls.wt("*Boundary\nBOT"+sufix+", 3, 3, {}".format(displ) )
                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ) )
                ls.wt("*Boundary\nBOT"+sufix+", 1, 2, 0" )

        # 6: TOP is displace
        elif type_bc == 6:
                # TOP is displaced in z direction and x and y are fixed
                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ/2) )
                ls.wt("*Boundary\nBOT"+sufix+", 3, 3, {}".format(-displ/2) )
                # Fix one point in BOT
                # PCIRC_TOP_48_CENTER
                ls.wt("*Boundary\nTOP_1, 1, 2, 0" )
                ls.wt("*Boundary\nTOP_16, 1, 2, 0" )

        else:
                raise ValueError("type_bc not valid")
    else:
        ls.wt("**Cylindrical Coordinates" )

        if type_bc == 1:
                # TOP
                # r     = 0 is fixed, 
                # theta is free,
                # z     is fixed
                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ) )
                ls.wt("*Boundary\nTOP"+sufix+", 1, 1, 0" )
                # All nodes in BOT are fixed
                ls.wt("*Boundary\nBOT"+sufix+", 1, 3, 0" )

        elif type_bc == 2:
                # TOP
                # r is free,
                # theta is fixed,
                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ) )
                ls.wt("*Boundary\nTOP"+sufix+", 2, 2, 0" )
                # BOT
                # r is free,
                # theta is fixed,
                # z is fixed
                ls.wt("*Boundary\nBOT"+sufix+", 3, 3, 0" )
                ls.wt("*Boundary\nBOT"+sufix+", 2, 2, 0" )
        elif type_bc == 3:
               # TOP
               # r is free,
               # theta is free,
                 # z is fixed
                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ) )
                # BOT
                # r is free,
                # theta is fixed,
                # z is fixed
                ls.wt("*Boundary\nBOT"+sufix+", 3, 3, 0" )

        elif type_bc == 6:
                # TOP is displaced in z direction and x and y are fixed
                # ls.wt("*Boundary\nTOP_CENTER"+sufix+", 2, 2, 0")
                # ls.wt("*Boundary\nBOT_CENTER"+sufix+", 2, 2, 0")

                ls.wt("*Boundary\nTOP"+sufix+", 3, 3, {}".format(displ/2) )
                ls.wt("*Boundary\nBOT"+sufix+", 3, 3, {}".format(-displ/2) )
                ls.wt("*Boundary\nBOT_CENTER"+sufix+", 2, 2, 0")
                ls.wt("*Boundary\nTOP_CENTER"+sufix+", 2, 2, 0")

                # Fix one point in BOT
                # PCIRC_TOP_48_CENTER
                #topfix = np.arange(1,64,4)
                #for i in topfix:
                #        ls.wt("*Boundary\nTOP_"+str(i)+", 2, 2, 0" )
                # ls.wt("*Boundary\nTOP"+sufix+", 2, 2, 0" )
                # ls.wt("*Boundary\nMID_POINTS, 2, 2, 0" )
        else:
                raise ValueError("type_bc not valid")

    # ====================================================
    # *** Loads ***
    # ====================================================
    ls.wt("*Cload, op=New"          )
    ls.wt("*Dload, op=New"          )
    ls.wt("*Node file"              )
    ls.wt("RF, U,"                  )
    ls.wt("*El file"                )
    ls.wt("S, E, EVOL"              )
    ls.wt("*Contact file"           )
    ls.wt("CDIS, CSTR, PCON"        )
    ls.wt("*EL PRINT, ELSET=ALL"    )
    ls.wt("EVOL"                    )
    ls.wt("*End step"               )

    return ls