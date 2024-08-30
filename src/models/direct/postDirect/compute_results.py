import pandas as pd
import os
from tools.basic.loadsavejson import  loadjson
from models.direct.postDirect.post_processing import post_processing

def compute_results(df,id,max_mono=1000,force_recompute=False):
    
    
    parametrize_path = df["main_path_abs"].values[id]

    vars_add = ["sigma","sigma_max","ratio"]

    simus = [ os.path.join(path,"simulation") 
            for path in df["paths"].values[id] ]
    parametrize_json = loadjson(os.path.join(parametrize_path,"vars.json"))

    results = []
    for simu in simus:
        try:
            results.append(post_processing(simu,max_mono=max_mono,force_recompute=force_recompute))
        except:
            results.append(None)
            print("Error in",simu)

    df_parametrize = parametrize_json["df"]
    ndata       = len(results)
    df_parametrize = df_parametrize.iloc[:ndata]

    for ivar in vars_add:
        sigmas = [ result[ivar] if type(result)==dict else None 
                  for result in results ]

        # add empyt row to have the same size
        df_parametrize = pd.concat([df_parametrize,
                                    pd.DataFrame(sigmas,
                                                columns=[ivar])],axis=1)
    return df_parametrize,results