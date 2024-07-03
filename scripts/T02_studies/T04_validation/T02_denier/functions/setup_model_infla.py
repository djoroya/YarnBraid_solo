
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


    out_inflat = os.path.join(main_path,"inflation")

    # save params as init.json
    createFolder(main_path)

    init_path = os.path.join(main_path,"init.json")
    savejson(params,init_path)


    params_gmsh     = params["gmsh"]
    params_infl     = params["inflation"]

    callback(nstep=1) if callback else None
    
    # STEP 4: Run inflation
    print_header("Running inflation")
    print_header("====================================")

    RunInflation(params_infl,out_inflat)
    callback() if callback else None
    # =======================================



    return params