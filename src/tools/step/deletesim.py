import shutil,os
join = os.path.join
from settings.simulations import simulations
from tools.basic.loadsavejson import loadjson
def deletesim(json_file):
    
    sim_params = loadjson(json_file)

    simulation_path = sim_params["simulation_path"]

    sim_path_abs = join(simulations(),simulation_path)

    if os.path.exists(sim_path_abs):
        shutil.rmtree(sim_path_abs)
        print("Simulation deleted")
        # remove json file
        os.remove(json_file)
        print("Initial json file deleted")
    else:
        print("Simulation not found")
    