import shutil,os
join = os.path.join
from settings.simulations import simulations
from tools.basic.loadsavejson import loadjson
def deletesim(json_file):
    
    sim_params = loadjson(json_file)
    simulation_path = sim_params["simulation_path"]
    delete_sim_key(simulation_path)

    
def delete_sim_key(simulation_path):

    sim_path_abs = join(simulations(),simulation_path)

    sim_params_path = join(sim_path_abs,"init.json")
    if not os.path.exists(sim_params_path):
        print("Simulation {} not found".format(simulation_path))
        return
    else:
        sim_params   = loadjson(sim_params_path)

    if os.path.exists(sim_path_abs):

        if sim_params["has_children"]:
            print("==============================")
            print("Simulation {} has children".format(simulation_path))
            # load params 
            params = loadjson(join(sim_path_abs,"params.json"))
            dependencies = params["dependencies"]
            for ikey in dependencies.keys():
                isimkey = dependencies[ikey]
                delete_sim_key(isimkey)

            print("Children of {} deleted".format(simulation_path))
            print("==============================")

        shutil.rmtree(sim_path_abs)
        print("Simulation {} deleted".format(simulation_path))

    else:
        print("Simulation {} not found".format(simulation_path))
