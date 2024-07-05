
from tools.basic.loadsavejson import loadjson
import importlib,os
from settings.simulations import simulations
import glob
import shutil
join = os.path.join

simulation_path = simulations()
def rerun(json_path,overwrite=False):

    
    sims = glob.glob(join(simulations(),"*"))
    sims = [os.path.basename(i) for i in sims]

    json_path     = os.path.abspath(json_path)
    json_path_rel = os.path.relpath(json_path)
    data = loadjson(json_path)

    if data["simulation_path"] in sims:
        if not overwrite:
            raise ValueError("Simulation exists. If you want to overwrite it, set overwrite=True")
        else:
            print("Simulation exists. It will be overwritten")
            folder_remove = join(simulations(),data["simulation_path"])
            shutil.rmtree(folder_remove)
        # Importar el módulo de la función
    else:
        print("Simulation does not exist. It will be created")
                                            
    default_path = data["function"]["file"].split(".")[:-1] + ["default"]
    model_module   = importlib.import_module(data["function"]["file"])
    module_default = importlib.import_module(".".join(default_path))
        
        # Obtener la función desde el módulo
    default_params = getattr(module_default, "default")()
    model = getattr(model_module, data["function"]["name"])
    for key in default_params.keys():
        if key in data.keys():
            default_params[key] = data[key]

    default_params["simulation_path"] =  data["simulation_path"]

    outfolder = json_path_rel.split(os.sep)[:-1]
    print(outfolder)
    model(default_params,outfolder)


