
from model.default          import *

import shutil,os

from models.direct.lammpshard.RunLammps         import RunLammps

from models.direct.GmshSplit.RunGmshSplit import RunGmshSplit
from models.direct.InflationDirect.RunInflationDirect import RunInflationDirect
from models.direct.simulationDirect.RunSimulation import RunSimulation
from models.direct.postDirect.RunPost import RunPost
import colorama
from tools.step.runstep             import   runstep,address,lj
def print_header(header):
    print(colorama.Fore.GREEN + header + colorama.Style.RESET_ALL)

@runstep(address(__file__))
def RunYB(params,main_path,callback=None):

    out_lammps = [*main_path,"temp","lammps"     ]
    out_gmsh   = [*main_path,"temp","gmsh"       ]
    out_inflat = [*main_path,"temp","inflation"  ] 
    out_simula = [*main_path,"temp","simulation" ]
    out_post   = [*main_path,"temp","post"       ]


    params_lmp      = params["lammps_sim"]
    params_gmsh     = params["gmsh"]
    params_infl     = params["inflation"]
    params_simula   = params["simulation"]
    params_post     = params["post"]

    callback(nstep=6) if callback else None


    # STEP 1: Run lammps
    print_header("Running lammps")
    print_header("====================================")
    params_lmp["settings_step"]["has_parent"] = True
    if "simulation_path" in params_lmp:
        params_lmp = lj(params_lmp["simulation_path"])
    else:
        RunLammps(params_lmp,out_lammps)

    callback() if callback else None
    # =======================================


    # STEP 2: Run gmsh
    print_header("Running gmsh")
    print_header("====================================")

    params_gmsh["lammps_path"] = params_lmp["simulation_path"]
    params_gmsh["settings_step"]["has_parent"] = True
    if "simulation_path" in params_gmsh:
        params_gmsh = lj(params_gmsh["simulation_path"])
    else:
        RunGmshSplit(params_gmsh,out_gmsh)
    callback() if callback else None
    # =======================================

    # STEP 3: Run inflation
    print_header("Running inflation")
    print_header("====================================")

    params_infl["gmsh_path"]  =  params_gmsh["simulation_path"] 
    params_infl["settings_step"]["has_parent"] = True
    if "simulation_path" in params_infl:
        params_infl = lj(params_infl["simulation_path"])
    else:
        RunInflationDirect(params_infl,out_inflat)
    callback() if callback else None
    # =======================================

    # STEP 4: Run simulation
    print_header("Running simulation")
    print_header("====================================")

    params_simula["inflation_path"] = params_infl["simulation_path"]
    params_simula["settings_step"]["has_parent"] = True
    if "simulation_path" in params_simula:
        params_simula = lj(params_simula["simulation_path"])
    else:
        RunSimulation(params_simula,out_simula)
    callback() if callback else None
    # =======================================

    # STEP 5: Run post
    print_header("Running post")
    print_header("====================================")

    params_post["tensile_path"] = params_simula["simulation_path"]
    params_post["settings_step"]["has_parent"] = True
    RunPost(params_post,out_post)
    callback() if callback else None
    # =======================================

    depen = dict()
    depen["lmp_path"]     = params_lmp["simulation_path"]
    depen["gmsh_path"]    = params_gmsh["simulation_path"]
    depen["infl_path"]    = params_infl["simulation_path"]
    depen["tensile_path"] = params_simula["simulation_path"]
    depen["post_path"]    = params_post["simulation_path"]
    params["dependencies"] = depen

    # remove card simulations 
    temp_path = [*main_path,"temp"]
    temp_path = os.path.join(*temp_path)
    shutil.rmtree(temp_path)


    return params