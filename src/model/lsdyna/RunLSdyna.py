import pandas as pd
import os

from model.lsdyna.lsdyna          import build_geo
from model.lsdyna.StartSamePlane  import StartSamePlane

from tools.basic.loadsavejson     import loadjson,savejson
from tools.step.runstep          import runstep
from tqdm.auto                   import tqdm
import shutil
import subprocess
import numpy as np
@runstep
def RunLSdyna(params,output_folder):

    out_folder = params["output_folder"]
    out_folder_abs = os.path.abspath(out_folder)
    params_lmp = loadjson(os.path.join(params['lmp_path'],"params.json"))

    params["npoints"] = int(params["factor_npoints"]*params_lmp["Npoints"])

    if params["hmax"] is not None:
        # recompute npoints to mach hmax
        hcurr = params["factor_npoints"]*params_lmp["h"]
        hmax    = params["hmax"]
        if hcurr>hmax:
            # hcurr -> factor_npoints
            # hmax  -> new_factor_npoints
            new_factor_npoints = params["factor_npoints"]*hmax/hcurr
            params["factor_npoints"] = new_factor_npoints
            params["npoints"] = int(new_factor_npoints*params_lmp["Npoints"])


    file_name = params_lmp["ParseLmp"]
    nhilos = params_lmp["nhilos"]
    
    if params["radius"] == None:
        #params["radius"] = 0.95*params_lmp["radius"]
        factor = params["factor"]
        params["radius"] = factor*params_lmp["r_hebra"]

    try:
        points  = pd.read_csv(file_name, header=0)
    except:
        file_name = os.path.join(params['lmp_path'],"data.csv")
        points  = pd.read_csv(file_name, header=0)

    if params['align']:
        # Proyectamos los punto iniciales y finales 
        # en el mismo plano
        # de manera que no tengamos problemas de contactos 
        points = StartSamePlane(points, params['npoints'],nhilos)
        params["old_points"] = params["npoints"]
        params["npoints"]    =  params["npoints"] + 2
        

    types   = points['type'].unique()
    npoints = params['npoints']

    # Seleccionar los primeros npoints de cada yarn
    # para la simulacion
    points_types = [points[points['type'] == itype].iloc[:npoints] 
                    for itype in types]
    lsdyna = params["lsdyna"]
    # Construir el comando para ejecutar lsdyna
    if os.name == 'nt':
        cmd =   '"'+lsdyna+'"'
    else:
        cmd =   lsdyna 

    cmd = cmd +" -nographics -nograph -nologo -batch main_XX.cfile > main_XX.log"
    # Se reemplaza XX por el numero de yarn
    # y FOLDER_VAR por la carpeta de salida

    cmd = cmd.replace('FOLDER_VAR', out_folder_abs)

    points_types = pd.concat(points_types)

    # Guardar el archivo params.json
    # Antes de iniciar la simulacion
    # por si ocurre un error
    json_file = os.path.join(output_folder,"params.json")
    savejson(params,json_file)

    fcn = tqdm if params["verbose"] else lambda x: x
    
    hilo_central = params_lmp["hilo_central"]
    # remove last yarn 
    # because it is the central yarn
    if hilo_central>0:
        types = types[:-hilo_central]
    
    cur_dir = os.getcwd()
    for itype in fcn(types):
        # Seleccionar los puntos de un yarn en especifico itype
        df = points_types[points_types['type'] == itype]
        # construir el archivo main.cfile para cada yarn
        build_geo(df, out_folder_abs, 
                      params['radius'],
                      name="out{}".format(int(itype)))
        
        cmd_loop = cmd.replace('XX', str(int(itype)))

        os.chdir(out_folder_abs)
        # copy the main.cfile to main_XX.cfile.replace('XX', str(int(itype))
        shutil.copy("main.cfile","main_{}.cfile".format(int(itype)))
        error = os.system(cmd_loop)
        if error != 0:
            print("Error in yarn {}".format(int(itype)))
            print("Check log file")
            print("Remenber that if you are using ssh connection you must use -X option and open Xming in local machine")
            raise Exception("Error in yarn {}".format(int(itype)))
        os.chdir(cur_dir)
        # comprobar si el archivo .step
        # fue creado
        step_file = "out{}.step".format(int(itype))
        step_file_full = os.path.join(out_folder,step_file)
        if not os.path.isfile(step_file_full):
            print("Error in yarn {}".format(int(itype)))
            print("Check log file")
            raise Exception("Error in yarn {}".format(int(itype)))

    return params