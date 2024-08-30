
from model.default          import *

import os

from models.direct.lammpshard.RunLammps         import RunLammps
from model.traj2mesh.RunTraj2Mesh   import RunTraj2Mesh
from model.inflation.RunInflation   import RunInflation
from model.simulation.RunSimulation import RunSimulation
import colorama

def print_header(header):
    print(colorama.Fore.GREEN + header + colorama.Style.RESET_ALL)

def RunYB_v2(params,main_path,callback=None):

    out_lammps = os.path.join(main_path,"lammps")
    out_t2m    = os.path.join(main_path,"traj2mesh")
    out_inflat = os.path.join(main_path,"inflation")
    out_simula = os.path.join(main_path,"simulation")


    params_lmp      = params["lammps"]
    params_t2m      = params["trajs2mesh"]
    params_infl     = params["inflation"]
    params_simula   = params["simulation"]

    callback(nstep=4) if callback else None


    # STEP 1: Run lammps
    print_header("Running lammps")
    print_header("====================================")
    RunLammps(params_lmp,out_lammps)
    callback() if callback else None
    # =======================================

    # STEP 2: Run traj2mesh
    print_header("Running traj2mesh")
    print_header("==================")

    params_t2m["lsdyna_params"]["lmp_path"] = params_lmp["output_folder"]
    RunTraj2Mesh(params_t2m,out_t2m)
    callback() if callback else None
    # =======================================


    # STEP 3: Run inflation
    print_header("Running inflation")
    print_header("====================================")

    params_infl["gmsh_path"]  =  params_t2m["gmsh_params"]["output_folder"] 
    RunInflation(params_infl,out_inflat)
    callback() if callback else None
    # =======================================

    # STEP 4: Run simulation
    print_header("Running simulation")
    print_header("====================================")

    params_simula["inflation_path"] = params_infl["output_folder"]
    RunSimulation(params_simula,out_simula)
    callback() if callback else None
    # =======================================

    return params