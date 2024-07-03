from tools.calculix.inp.inp import inp
import os
from tools.calculix.read_dat import read_dat

def CreateDeformedInp(params):

        inflation_folder = params["output_folder"]
        output_folder    = params["output_folder"]
        # Load de inp of inflation
        # ==============================================================================
        dat_file = os.path.join(inflation_folder,"init.dat")
        # Load the dat file

        dat = read_dat(dat_file) # ["displacements"]["df"]
        dat = [ ir for ir in dat if ir["name"] == "displacements" ][0]
        dat = dat["df"]
        #firrst column will be a index
        dat = dat.set_index("nid")
        # column names x y z and index name is "nid"
        dat.columns = ["x","y","z"]
        dat.index.name = "nid"

        inp_file = os.path.join(inflation_folder,"init.inp")
        inp_f = inp(inp_file,warning=False)
        # update the nodes dataframe. We sum nodes position with displacement
        inp_f.nodes.df = inp_f.nodes.df + dat

        # homotecia
        # ==============================================================================
        params_infl = params
        radius_target = params_infl["r_hebra"]
        radius_init   = params_infl["yarn_radius"]
        # factor of homotecia
        factor = radius_target/radius_init
        # homotecia
        inp_f.nodes.df = inp_f.nodes.df*factor

        # measure z 
        z_min = inp_f.nodes.df["z"].min()
        z_max = inp_f.nodes.df["z"].max()
        params["height"] = z_max - z_min
        #
        params["yarn_radius_homotecia"] = factor*params_infl["yarn_radius"] 
        params["hometecia"] = factor
        #       
        # ==============================================================================
        # load old inp file
        # ==============================================================================
        inp_dir = os.path.join(inflation_folder,"init.inp")
        # load lines of text file
        with open(inp_dir) as f:
            lines = f.readlines()


        # find * lines 
        indx = [i for i, s in enumerate(lines) if '*' in s]
        # find *step line
        indx_step = [i for i, s in enumerate(lines) if s.startswith('*Step')]

        indx_step = indx_step[0]

        lines_without_nodes =   lines[indx[1]:indx_step] 
        lines_with_new_nodes = [inp_f.nodes.print() , lines_without_nodes]
        # join lines
        lines_with_new_nodes = [item 
                                for sublist in lines_with_new_nodes 
                                for item in sublist]

        # write new inp file
        file_out = os.path.join(output_folder,"deformed.inp")
        with open(file_out, "w") as f:
            for line in lines_with_new_nodes:
                f.write(line)

        return params_infl