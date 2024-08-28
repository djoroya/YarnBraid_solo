import os
from tools.step.runstep import runstep,lj,address
import numpy as np
from model.GmshSplit.functions.genesq import genesq
from model.GmshSplit.functions.gmsh import gmsh_mesh
from model.lammps.traj2df import traj2df
join = os.path.join


@runstep(address(__file__))
def RunGmshSplit(params,output_folder):

    lammps_path = params["lammps_path"]

    params_lmp = lj(lammps_path)
    params_lmp["r0"] = params_lmp["r_hebra"]
    r0 = params_lmp["r0"]*params["factor_radius"]

    trajs = params_lmp["df"]
    trajs = [trajs[trajs["type"] == i][["xu","yu","zu"]].values
            for i in trajs["type"].unique()]
    
    zmax = np.max([np.max(traj[:,2]) for traj in trajs])
    zmin = np.min([np.min(traj[:,2]) for traj in trajs])
    Lz = zmax - zmin
    Lz = Lz*params["factor_length"]
    Lz_mean = 0.5*(zmax + zmin)

    for i in range(len(trajs)):
        # cut trajs to Lz
        bools = trajs[i][:,2] < Lz_mean + 0.5*Lz 
        bools = bools & (trajs[i][:,2] > Lz_mean - 0.5*Lz)
        trajs[i] = trajs[i][bools,:].copy()
        
    #ntrajs = [ len(traj) for traj in trajs ]
    #id_trajs = [ int(ntraj*factor_length) for ntraj in ntrajs ]
    #trajs = [ traj[:id_traj] for traj, id_traj in zip(trajs, id_trajs) ]


    trajs = [ trajs[i] for i in range(64)] #hardcoded 64 

    params["trajs"] = traj2df(trajs)

    params["MeshSizeMin"] = params["factor_mesh_min"]*r0
    params["MeshSizeMax"] = params["factor_mesh_max"]*r0

    inp_obj = []
    iterations = 1

    for itraj in trajs:
        print("Trajectory ",iterations)
        iterations += 1
        debug = False
        inp_obj_loop = gmsh_mesh(itraj,r0,params,debug=debug)

        inp_obj.append(inp_obj_loop)



    df = params["trajs"]
    df = [df.loc[df["type"]==i] for i in np.unique(df["type"])]


    genesq(inp_obj,df,r0)
    N = len(inp_obj)

    for i in range(N):
        inp_obj[i].print(join(params["output_folder"],
                              "mesh" + str(i) + ".inp"))
    for i in range(1,N):
        inp_obj[0].merge(inp_obj[i], prefix="P"+str(i+1)+"_")


    inp_obj[0].print(join(params["output_folder"],"init.inp"))
