
from model.default          import *

import os

from model.lsdyna.RunLSdyna         import RunLSdyna
from model.gmsh.RunGmsh             import RunGmsh
from tools.step.runstep          import runstep

import colorama
from tools.basic.loadsavejson     import loadjson

def print_header(header):
    print(colorama.Fore.GREEN + header + colorama.Style.RESET_ALL)

@runstep
def RunTraj2Mesh(params,main_path):

    out_lsdyna = os.path.join(main_path,"lsdyna")
    out_gmsh   = os.path.join(main_path,"gmsh")

    params_lsdyna   = params["lsdyna_params"]
    params_gmsh     = params["gmsh_params"]

    # =======================================
    # STEP 2: Run lsdyna
    print_header("Running lsdyna")
    print_header("====================================")

    RunLSdyna(params_lsdyna,out_lsdyna)
    # =======================================
    # STEP 3: Run gmsh
    print_header("Running gmsh")
    print_header("====================================")

    params_gmsh["lsdyna_path"] = params_lsdyna["output_folder"]
    RunGmsh(params_gmsh,out_gmsh)
    # =======================================


    return params