import os
from tools.step.runstep import runstep,lj,address
import numpy as np
from models.direct.GmshSplit.functions.genesq import genesq
from models.direct.GmshSplit.functions.gmsh import gmsh_mesh
from models.direct.lammpshard.traj2df import traj2df
from models.direct.GmshSplit.createalma import createalma
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
        bools = trajs[i][:,2] <= Lz_mean + 0.5*Lz 
        bools = bools & (trajs[i][:,2] >= Lz_mean - 0.5*Lz)
        trajs[i] = trajs[i][bools,:].copy()
        

    # =============================================================================
    le = 0.5
    if False:
        for i in range(64):
            r0 = trajs[i][0].copy()
            rf = trajs[i][-1].copy()

            # igual x,y and change z 
            r0_new = np.array([r0[0],r0[1],r0[2] + le])
            rf_new = np.array([rf[0],rf[1],rf[2] - le])
            #
            Nsteps = 10
            r0_list = [ r0 + (r0 - r0_new) * (j / Nsteps)**0.9 for j in range(1,Nsteps)]
            r0_list = np.vstack(r0_list)
            # reverse 
            r0_list = r0_list[::-1]
            rf_list = [ rf + (rf - rf_new) * (j / Nsteps)**0.9 for j in range(1,Nsteps)]
            rf_list = np.vstack(rf_list)
            # reverse
            # round 5 decimals
            r0_list = np.round(r0_list,5)
            rf_list = np.round(rf_list,5)

            trajs[i] = np.vstack([r0_list,trajs[i][1:-1],rf_list])

    # =============================================================================
    #ntrajs = [ len(traj) for traj in trajs ]
    #id_trajs = [ int(ntraj*factor_length) for ntraj in ntrajs ]
    #trajs = [ traj[:id_traj] for traj, id_traj in zip(trajs, id_trajs) ]


    trajs = [ trajs[i] for i in range(64)] #hardcoded 64 
    zmax = np.max([np.max(traj[:,2]) for traj in trajs])
    zmin = np.min([np.min(traj[:,2]) for traj in trajs])
    almatrajs = createalma(params["Nalma"],zmin,zmax)
    ## extend trajs
    trajs.extend(almatrajs)


    # # añadimos un penuultimo punto a cada trayectoria, este sera el punto medio entre el penultimo y el ultimo
    # for k in range(1):
    #     for i in range(len(trajs)):
    #         penultimate_point = trajs[i][-2].copy()
    #         last_point = trajs[i][-1].copy()
    #         rmu = 0.1*penultimate_point + 0.9*last_point
    #         trajs[i] = np.vstack([trajs[i][:-1],rmu,last_point])

    params["trajs"] = traj2df(trajs)

    params["MeshSizeMin"] = params["factor_mesh_min"]*r0
    params["MeshSizeMax"] = params["factor_mesh_max"]*r0

    inp_obj = []
    iterations = 1
    list_index_l = []
    for itraj in trajs:
        print("Trajectory ",iterations)
        iterations += 1
        debug = False
        inp_obj_loop,list_index = gmsh_mesh(itraj,r0,params,debug=debug)

        inp_obj.append(inp_obj_loop)
        list_index_l.append(list_index)


    for i in range(len(trajs)):
        newtrajs = trajs[i].copy()

        lastpoint = newtrajs[-1]
        penultimo = newtrajs[-2]
        newtrajs = newtrajs[:(list_index_l[i][-2]+1)]
        newpenultimo = newtrajs[-1]

        # create a list of points between lastpoint and newlastpoint 
        npoints = 6
        points = np.linspace(newpenultimo,penultimo,npoints)

        trajs[i]  = np.vstack([newtrajs,points[1:],lastpoint])


    params["trajs"] = traj2df(trajs)

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
