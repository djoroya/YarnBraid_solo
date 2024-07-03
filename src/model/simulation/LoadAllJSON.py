from tools.basic.loadsavejson    import savejson, loadjson


def LoadAllJSON(json_path_file):

    # json_path_file must be a list of json paths

    params = [ loadjson(ijson) for ijson in json_path_file ]

    params_gmsh = [ loadjson(ip["gmsh_path"]) for ip in params ]

    params_lsdy = [ loadjson(ip["lsdyna_path"]) for ip in params_gmsh ]

    params_lmp  = [ loadjson(ip["lmp_path"]+"params.json") 
                   for ip in params_lsdy ]


    for i,ip in enumerate(params):
        ip["gmsh"]   = params_gmsh[i]
        ip["lsdyna"] = params_lsdy[i]
        ip["lmp"]    = params_lmp[i]

    return params