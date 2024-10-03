from tools.calculix.inp.inp import inp
import pandas as pd
import os
from tools.basic.loadsavejson     import loadjson
import numpy as np
from tools.calculix.read_dat import read_dat
from models.direct.simulationDirect.addStep import addStep
from settings.simulations import simulations
class lines_obj():
    def __init__(self):
        self.lines = ""
    def wt(self,line):
        self.lines = self.lines + line + "\n"

join = lambda *args: os.path.join(*args)

def build_inp(params):

        inflation_folder = params["inflation_path"]
        inflation_folder = join(simulations(),inflation_folder)
        output_folder    = params["output_folder"]
        # Load de inp of inflation
        # ==============================================================================
        dat_file = join(inflation_folder,"init.dat")
        # Load the dat file
        data = read_dat(dat_file)
        # select displacements
        data_select = [s for s in data if s["name"] == "displacements"][-1]
        dat = data_select["df"]
        #firrst column will be a index
        dat = dat.set_index("nid")
        # column names x y z and index name is "nid"
        dat.columns = ["x","y","z"]
        dat.index.name = "nid"

        inp_file = join(inflation_folder,"init.inp")
        inp_f = inp(inp_file,warning=False)
        # update the nodes dataframe. We sum nodes position with displacement
        inp_f.nodes.df = inp_f.nodes.df + dat

        # ==============================================================================
        json_infl = join(inflation_folder,"params.json")
        params_infl = loadjson(json_infl)
        # ==============================================================================
        # measure z 
        z_min = inp_f.nodes.df["z"].min()
        z_max = inp_f.nodes.df["z"].max()
        params["height"] = z_max - z_min
        epsilon = params["epsilon"]
        params["displacement"] = params["height"]*epsilon
        # ==============================================================================

        #       
        # ==============================================================================
        # load old inp file
        # ==============================================================================
        inp_dir = join(inflation_folder,"init.inp")
        # load lines of text file
        with open(inp_dir) as f:
            lines = f.readlines()

        # ==============================================================================
        # remove *EQUATION CARD
        #for this find * in lines
        # indx_card = [i for i, s in enumerate(lines)
        #              if s.startswith('*')]
        # # of this lines find *EQUATION CARD
        # indx_eq = [i for i, s in enumerate(indx_card)
        #            if lines[s].startswith('*EQUATION')]

        # start = indx_card[indx_eq[0]]
        # end   = indx_card[indx_eq[-1]+1]

        # lines = lines[:start] + lines[end:]

        # 
        # bot_nset_rep = inp_f.select_regex(".*REP.*","nset")
        bot_nset = inp_f.select_regex("BOT.*","nset")
        bot_nset = bot_nset[:64]
        top_nset = inp_f.select_regex("TOP.*","nset")
        top_nset = top_nset[:64]

        # top_center = inp_f.select_regex(".*TOP.*CENTER.*","nset")
        # bot_center = inp_f.select_regex(".*BOT.*CENTER.*","nset")

        # ==============================================================================
        all_bonds = params_infl["all_bonds"]
        for bond in all_bonds:

            top_nset_master = top_nset[bond[0]-1]
            # bot_nset_slave  = bot_nset_rep[bond[1]-1]
            bot_nset_slave  = bot_nset[bond[1]-1]
            
            # inp_f.AddEquation(top_nset_master.name,
            #                   bot_nset_slave.name ,
            #                   type_eq="linear_interpolation",
            #                   nodes=inp_f.nodes.df,
            #                   dims=[1,2])

        # ==============================================================================
        midpoints = inp_f.select_regex("MID_POINTS","nset")

        # inp_f.AddEquation(midpoints[0].name,
        #                   midpoints[0].name,
        #                   type_eq="set_center_mass",
        #                   dims=[1,2])

        # ==============================================================================
        # New Nset
        center_name = ["TOP","BOT"]
        lines_nset = "\n"
        for name in center_name:
             
            lines_nset = lines_nset+"*Nset, nset={}_CENTER\n".format(name)
            for i in range(64):
                lines_nset = lines_nset + "PCIRC_{}_{}_CENTER , ".format(name,i+1)
                if (i+1)%10 == 0:
                    lines_nset = lines_nset + "\n"
            lines_nset = lines_nset + "\n"

        lines_eq = [card.print()+"\n" for card in inp_f.equations]
        # merge lines_eq with lines
        # ==============================================================================
        # add adjust paramter in *Contact pair
        # "Type=Surface to surface" -> "Type=Surface to surface, Adjust={}"
        Adjust = params["Adjust"]
        if Adjust:
                Adjust = params_infl["r_hebra"]*0.001 # 0.1% of yarn radius
                lines = [line.replace("Type=Surface to surface",
                                "Type=Surface to surface, Adjust={}".format(Adjust)) 
                                for line in lines]
        # find * lines 
        indx = [i for i, s in enumerate(lines) if '*' in s]
        # find *step line
        indx_step = [i for i, s in enumerate(lines) 
                       if s.startswith('*Step')]

        indx_step = indx_step[0]
        #      
        if params["cylindrical"]:
            if params["only_braid"]:
                 sufix = "_BRAID"
            else:
                sufix = ""
            lines_trans =                "*TRANSFORM, NSET=BOT"+sufix+", TYPE=C\n"
            lines_trans = lines_trans  + "0,0,0,0,0,1\n"	
            lines_trans = lines_trans  + "*TRANSFORM, NSET=TOP"+sufix+", TYPE=C\n"
            lines_trans = lines_trans  + "0,0,0,0,0,1\n"	

        else:
            lines_trans = "**\n"

        if params["surface_interaction"]["type"] == "linear":
            line_replace    ="*Surface interaction, Name=SURFACE_INTERACTION_1\n*Surface behavior, Pressure-overclosure=linear"
            factor_E = params["surface_interaction"]["factor_E"]
            K = factor_E*params["young"]     
            line_replace    = line_replace + "\n{},0,0\n".format(K)

        lines_midpoints_tranform = "*TRANSFORM, NSET=MID_POINTS, TYPE=C\n"
        lines_midpoints_tranform = lines_midpoints_tranform + "0,0,0,0,0,1\n"

        for i in range(64):
            lines_midpoints_tranform = lines_midpoints_tranform +"*TRANSFORM, NSET=MID_POINT_{} , TYPE=C\n".format(i+1)
            lines_midpoints_tranform = lines_midpoints_tranform + "0,0,0,0,0,1\n"

        lines_tie = ""

        if params_infl["ties_activate"]:
            ties = params_infl["ties"]
            for i in range(len(ties)):
                lines_tie = lines_tie + "*Tie, Name=TIE_{}\n".format(i+1)
                lines_tie = lines_tie + "SURFACE_{}, SURFACE_{}\n".format(ties[i][0],ties[i][1])



        # =========================================================================
        # Add step
        # =========================================================================
        nsteps = params["nsteps"]
        # nsteps = 1 assert "nsteps must be greater than 1"
        assert nsteps > 1, "nsteps must be greater than 1"
        nruns  = params["nruns"]
        nsets  = params_infl["nsets"]
        
        ls_list = []
        #first_di = 0.001*params["displacement"]
        first_di = 0.1*params["displacement"]
        di_span = np.linspace(first_di,params["displacement"],nsteps*nruns)
        di_span = np.append(di_span,params["displacement"])
        iter = -1
        for i in range(nruns):
            ls = lines_obj()
            for j in range(nsteps):
                iter = iter + 1
                di = di_span[iter]
                # round to 3 decimals
                di = round(di,5)
                ls = addStep(ls,nsets,params,di)
                # remove *Contact file output
                # ls.lines = ls.lines.replace("*Contact file\nCDIS, CSTR, PCON\n",
                #                             "*Contact file\nPCON\n")
                
            ls_list.append(ls)

            file = join(output_folder,"step_"+str(i+1)+".inp")
            # save all ls lines
            with open(file, "w") as f:
                    for line in ls.lines:
                            f.write(line) 

        # =========================================================================
                        
        # Search *Elastic
        indx_elastic = [i for i, s in enumerate(lines) 
                        if s.startswith('*Elastic')]

        young   = params["young"]
        poisson = params["poisson"]
        lines[indx_elastic[0]+1] = "{},{}\n".format(young,poisson)

        lines_without_nodes =   lines[indx[1]:indx_step] 

        if params["surface_interaction"]["type"] == "linear":
            # find line *SURFACE INTERACTION
            indx_surface_interaction = [i for i, s in enumerate(lines_without_nodes) 
                                        if s.startswith('*Surface interaction, Name=')] 
            # replace line
            lines_without_nodes[indx_surface_interaction[0]] = line_replace 
            lines_without_nodes[indx_surface_interaction[0]+1] = "\n"
            
        lines_with_new_nodes = [inp_f.nodes.print() , 
                                lines_eq,
                                lines_without_nodes, 
                                lines_trans,
                                lines_midpoints_tranform,
                                lines_nset,
                                lines_tie,
                                ls_list[0].lines]
        # join lines
        lines_with_new_nodes = [item 
                                for sublist in lines_with_new_nodes 
                                for item in sublist]

        # write new inp file
        file_out = join(output_folder,"init_new.inp")
        with open(file_out, "w") as f:
            for line in lines_with_new_nodes:
                f.write(line)
            
        # ==============================================================================
        if nruns>1:
            for i in range(2,nruns+1):
                file_name = join(output_folder,
                                "init_new_{}.inp".format(i))
                file = open(file_name,"w")
                #file.write("*RESTART,READ,STEP="+ str(nsteps*(i-1)) +"\n")
                file.write("*RESTART,READ\n")

                content = ls_list[i-1].lines
                file.write(content)

        return params_infl