
from model.default          import *

import os

from model.lammps.RunLammps         import RunLammps
from model.lsdyna.RunLSdyna         import RunLSdyna
from model.gmsh.RunGmsh             import RunGmsh
from model.inflation.RunInflation   import RunInflation
from tools.step.runstep import runstep
from tools.basic.loadsavejson import savejson
from tools.basic.createFolder import createFolder

import colorama

def print_header(header):
    print(colorama.Fore.GREEN + header + colorama.Style.RESET_ALL)

def setup_model(params,main_path,callback=None):

    out_lammps = os.path.join(main_path,"lammps")
    out_lsdyna = os.path.join(main_path,"lsdyna")
    out_gmsh   = os.path.join(main_path,"gmsh")
    out_inflat = os.path.join(main_path,"inflation")

    # save params as init.json
    createFolder(main_path)

    init_path = os.path.join(main_path,"init.json")
    savejson(params,init_path)

    params_lmp      = params["lammps"]
    params_lsdyna   = params["lsdyna"]
    params_gmsh     = params["gmsh"]
    params_infl     = params["inflation"]

    callback(nstep=4) if callback else None


    # STEP 1: Run lammps
    print_header("Running lammps")
    print_header("====================================")
    RunLammps(params_lmp,out_lammps)
    callback() if callback else None
    if params["only_lammps"]:
        return params
    # =======================================
    
    # STEP 2: Run lsdyna
    print_header("Running lsdyna")
    print_header("====================================")

    params_lsdyna['lmp_path']  = params_lmp["output_folder"]
    RunLSdyna(params_lsdyna,out_lsdyna)
    callback() if callback else None
    # =======================================
    

    # STEP 3: Run gmsh
    print_header("Running gmsh")
    print_header("====================================")

    params_gmsh["lsdyna_path"] = params_lsdyna["output_folder"]
    RunGmsh(params_gmsh,out_gmsh)
    callback() if callback else None
    # =======================================

    # STEP 4: Run inflation
    print_header("Running inflation")
    print_header("====================================")

    params_infl["gmsh_path"]  =  params_gmsh["output_folder"] 
    RunInflation(params_infl,out_inflat)
    callback() if callback else None
    # =======================================



    return params