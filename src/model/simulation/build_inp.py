from tools.calculix.inp.inp import inp
import pandas as pd
import os
from tools.basic.loadsavejson     import loadjson
import numpy as np
from tools.calculix.read_dat import read_dat
from model.simulation.addStep import addStep

class lines_obj():
    def __init__(self):
        self.lines = ""
    def wt(self,line):
        self.lines = self.lines + line + "\n"

join = lambda *args: os.path.join(*args)

def build_inp(params):

        inflation_folder = params["inflation_path"]
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
            lines_trans =                "*TRANSFORM, NSET=BOT, TYPE=C\n"
            lines_trans = lines_trans  + "0,0,0,0,0,1\n"	
            lines_trans = lines_trans  + "*TRANSFORM, NSET=TOP, TYPE=C\n"
            lines_trans = lines_trans  + "0,0,0,0,0,1\n"	

        else:
            lines_trans = "**\n"

        if params["surface_interaction"]["type"] == "linear":
            line_replace    ="*Surface interaction, Name=SURFACE_INTERACTION_1\n*Surface behavior, Pressure-overclosure=linear"
            factor_E = params["surface_interaction"]["factor_E"]
            K = factor_E*params["young"]     
            line_replace    = line_replace + "\n{},0,0\n".format(K)


        # =========================================================================
        # Add step
        # =========================================================================
        nsteps = params["nsteps"]
        nruns  = params["nruns"]
        nsets  = params_infl["nsets"]
        
        ls_list = []
        first_di = 0.001*params["displacement"]
        di_span = np.linspace(first_di,params["displacement"],nsteps*nruns)
        di_span = np.append(di_span,params["displacement"])
        iter = -1
        for i in range(nruns):
            ls = lines_obj()
            for j in range(nsteps):
                iter = iter + 1
                di = di_span[iter]
                # round to 3 decimals
                di = round(di,3)
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
                                lines_without_nodes, 
                                lines_trans,
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