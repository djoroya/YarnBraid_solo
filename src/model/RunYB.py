
from model.default          import *

import os

from model.lammps.RunLammps         import RunLammps
from model.lsdyna.RunLSdyna         import RunLSdyna
from model.gmsh.RunGmsh             import RunGmsh
from model.inflation.RunInflation   import RunInflation
from model.simulation.RunSimulation import RunSimulation
import colorama
from tools.step.runstep             import   runstep

def print_header(header):
    print(colorama.Fore.GREEN + header + colorama.Style.RESET_ALL)

@runstep
def RunYB(params,main_path,callback=None):

    out_lammps = [*main_path,"lammps"     ]
    out_lsdyna = [*main_path,"lsdyna"     ]
    out_gmsh   = [*main_path,"gmsh"       ]
    out_inflat = [*main_path,"inflation"  ] 
    out_simula = [*main_path,"simulation" ]


    params_lmp      = params["lammps_sim"]
    params_lsdyna   = params["lsdyna_sim"]
    params_gmsh     = params["gmsh"]
    params_infl     = params["inflation"]
    params_simula   = params["simulation"]

    callback(nstep=5) if callback else None


    # STEP 1: Run lammps
    print_header("Running lammps")
    print_header("====================================")
    RunLammps(params_lmp,out_lammps)
    callback() if callback else None
    # =======================================

    # STEP 2: Run lsdyna
    print_header("Running lsdyna")
    print_header("====================================")

    params_lsdyna['lmp_path']  = params_lmp["simulation_path"]
    RunLSdyna(params_lsdyna,out_lsdyna)
    callback() if callback else None
    # =======================================


    # STEP 3: Run gmsh
    print_header("Running gmsh")
    print_header("====================================")

    params_gmsh["lsdyna_path"] = params_lsdyna["simulation_path"]
    RunGmsh(params_gmsh,out_gmsh)
    callback() if callback else None
    # =======================================

    # STEP 4: Run inflation
    print_header("Running inflation")
    print_header("====================================")

    params_infl["gmsh_path"]  =  params_gmsh["simulation_path"] 
    RunInflation(params_infl,out_inflat)
    callback() if callback else None
    # =======================================

    # STEP 5: Run simulation
    print_header("Running simulation")
    print_header("====================================")

    params_simula["inflation_path"] = params_infl["simulation_path"]
    RunSimulation(params_simula,out_simula)
    callback() if callback else None
    # =======================================

    params["lmp_path"]     = params_lmp["simulation_path"]
    params["lsdyna_path"]  = params_lsdyna["simulation_path"]
    params["gmsh_path"]    = params_gmsh["simulation_path"]
    params["infl_path"]    = params_infl["simulation_path"]
    params["tensile_path"] = params_simula["simulation_path"]

    return params