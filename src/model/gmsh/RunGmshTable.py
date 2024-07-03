import os
from tools.step.runstep import runstep
from tools.basic.loadsavejson import loadjson
import numpy as np
from model.gmsh.genesq import genesq
from model.gmsh.gmsh import gmsh_mesh
join = os.path.join
lj   = lambda *x: loadjson(join(*x))

@runstep
def RunGmshTable(params,output_folder):

    lammps_path = params["lammps_path"]

    params_lmp = lj(lammps_path,"params.json")
    params_lmp["r0"] = params_lmp["r_hebra"]
    r0 = params_lmp["r0"]*params["factor_radius"]



    trajs = params_lmp["df"]
    trajs = [trajs[trajs["type"] == i][["xu","yu","zu"]].values
            for i in trajs["type"].unique()]
    


    params["MeshSizeMin"] = params["factor_mesh_min"]*r0
    params["MeshSizeMax"] = params["factor_mesh_max"]*r0

    inp_obj = []
    iterations = 1
    for itraj in trajs:
        print("Trajectory ",iterations)
        iterations += 1
        
        args = (itraj,r0,output_folder,params)

        inp_obj_loop = gmsh_mesh(*args)

        inp_obj.append(inp_obj_loop)


    df = params_lmp["old_df"]
    df = [df.loc[df["type"]==i] for i in np.unique(df["type"])]


    genesq(inp_obj,df,r0)
    N = len(inp_obj)

    for i in range(N):
        inp_obj[i].print(output_folder + "/mesh" + str(i) + ".inp")

    for i in range(1,N):
        inp_obj[0].merge(inp_obj[i], prefix="P"+str(i+1)+"_")

    inp_obj[0].print(output_folder + "/init.inp")