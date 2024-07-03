# search vars.json
from tools.basic.loadsavejson import loadjson
import glob
import pandas as pd
import os
def explore(main_path):
    vars_path         = glob.glob(main_path + "/*/vars.json")
    vars_path_folders = glob.glob(main_path + "/*/")
    if os.name == 'nt':
        date = [ path.split("\\")[-2].split("__")[0:2] for path in vars_path_folders ]
    else:
        date = [ path.split("/")[-2].split("__")[0:2] for path in vars_path_folders ]
    vars_json = [ loadjson(path) for path in vars_path ]

    variable_study = [ [ ikey for ikey in vars_json[i]["vars"].keys()] for i in range(len(vars_json)) ]
    ncases         = [ len(vars_json[i]["df"]) for i in range(len(vars_json)) ]
    exe_cases      = [ len(vars_json[i]["paths"]) for i in range(len(vars_json)) ]
    paths          = [ vars_json[i]["paths"] for i in range(len(vars_json)) ]
    for i in range(len(vars_json)):
        vars_json[i]["study"] = variable_study[i]
        vars_json[i]["ncases"] = ncases[i]
        vars_json[i]["exe_cases"] = exe_cases[i]
        vars_json[i]["date"] = date[i]
        vars_json[i]["paths_folder"] = vars_path_folders[i]
        vars_json[i].pop("df")
        #vars_json[i].pop("paths")
        vars_json[i].pop("vars")

    vars_json = sorted(vars_json, key=lambda k: k['date'])
    paths = [ vars_json[i]["paths"] for i in range(len(vars_json)) ]

    df = pd.DataFrame(vars_json)
        # count number of cases
    return df,paths