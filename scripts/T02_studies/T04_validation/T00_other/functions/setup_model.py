
from model.default          import *

import os

from models.direct.lammpshard.RunLammps         import RunLammps
from model.lsdyna.RunLSdyna         import RunLSdyna
from model.Gmsh.RunGmsh             import RunGmsh
from model.inflation.RunInflation   import RunInflation
import colorama

def print_header(header):
    print(colorama.Fore.GREEN + header + colorama.Style.RESET_ALL)

def setup_model(params,main_path,callback=None):

    out_lammps = [*main_path,"lammps"]
    out_lsdyna = [*main_path,"lsdyna"]
    out_gmsh   = [*main_path,"gmsh"]
    out_inflat = [*main_path,"inflation"]


    params_lmp      = params["lammps_sim"]
    params_lsdyna   = params["lsdyna_sim"]
    params_gmsh     = params["gmsh"]
    params_infl     = params["inflation"]

    callback(nstep=4) if callback else None


    # STEP 1: Run lammps
    print_header("Running lammps")
    print_header("====================================")
    params_lmp["settings_step"]["has_parent"] = True

    RunLammps(params_lmp,out_lammps)
    callback() if callback else None
    if params["only_lammps"]:
        return params
    # =======================================
    
    # STEP 2: Run lsdyna
    print_header("Running lsdyna")
    print_header("====================================")

    params_lsdyna['lmp_path']  = params_lmp["simulation_path"]
    params_lsdyna["settings_step"]["has_parent"] = True

    RunLSdyna(params_lsdyna,out_lsdyna)
    callback() if callback else None
    # =======================================
    

    # STEP 3: Run gmsh
    print_header("Running gmsh")
    print_header("====================================")

    params_gmsh["lsdyna_path"] = params_lsdyna["simulation_path"]
    params_gmsh["settings_step"]["has_parent"] = True

    RunGmsh(params_gmsh,out_gmsh)
    callback() if callback else None
    # =======================================

    # STEP 4: Run inflation
    print_header("Running inflation")
    print_header("====================================")

    params_infl["gmsh_path"]  =  params_gmsh["simulation_path"] 
    params_infl["settings_step"]["has_parent"] = True

    RunInflation(params_infl,out_inflat)
    callback() if callback else None
    # =======================================

    return params