from tools.basic.loadsavejson import  loadjson
from tools.calculix.frd.readfrd      import  readfrd
import os
from tools.basic.loadsavejson import  loadjson
from tools.calculix.frd.readfrd      import  readfrd
import os
from tqdm import tqdm

def load_parametrize(main_path,avoid=None):
    vars_json = loadjson(os.path.join(main_path, "vars.json"))


    frds_list = []
    idx = []
    paths = vars_json["paths"]
    if avoid is not None:
        paths = paths[:-avoid]

    for i in tqdm(range(len(paths))):
        frd_path = os.path.join(paths[i],"simulation","init_new.frd")
        if os.path.exists(frd_path) and os.stat(frd_path).st_size > 10:
            frds_list.append(readfrd(frd_path))
            idx.append(i)
        
    # ==============================================================================
    inflation = [ os.path.join(paths[i],"inflation","params.json") 
                  for i in idx ]

    inflation_params = [ loadjson(inflation[i]) 
                        for i in range(len(inflation))]
    # 
    # simulation params
    #
    simulation = [ os.path.join(paths[i],"simulation","params.json") 
            for i in idx ]
    
    simulation_params = [ loadjson(simulation[i])
                        for i in range(len(simulation))]
    df = vars_json["df"]
    df = df.iloc[idx]
    df = df.reset_index(drop=True)

    return df,frds_list,inflation_params,vars_json,simulation_params

# ==============================================================================
