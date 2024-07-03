import glob
from tools.basic.loadsavejson     import loadjson

def GetAll_lsdyna():
    
    json_path_file = glob.glob("../02_LS_DYNA_PREPOST/output/*/*.json")
    jsons = []
    for path in json_path_file:
        try:
            jsons.append(loadjson(path))
        except:
            print("The file {} is not a json file".format(path))
            pass

    return jsons