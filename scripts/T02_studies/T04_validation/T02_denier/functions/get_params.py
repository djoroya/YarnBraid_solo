import os
from tools.basic.loadsavejson import loadjson
from model.inflation.ComputeDenier import ComputeDenier

join = os.path.join

def get_params(paths):   
    paths = [ path for path in paths 
             if os.path.exists(join(path,"inflation","params.json")) ]
    vars = [ loadjson(join(path,"inflation","params.json")) for path in paths ]

    for var in vars:
        ComputeDenier(var,4)
        
    if "final_time" not in vars[-1].keys():
        vars = vars[:-1]
        paths = paths[:-1]

    vars_lmp  = [ loadjson(join(var["gmsh_path"],"..","lammps","params.json"))
                 for var in vars ]

    deniers        = [ ivar["denier"]      for ivar in vars    ]
    yarn_radius    = [ ivar["yarn_radius"] for ivar in vars    ]
    hs             = [ ivar["height"]      for ivar in vars    ]
    theta          = [ ivar["theta"]       for ivar in vars_lmp]
    radius_max     = [ ivar["radius_max"]  for ivar in vars    ]
    denier_per_new = [ ivar["denier_per_filament"] for ivar in vars ]
    pressure       = [ ivar["pressure"]   for ivar in vars]
    if len(theta) > len(deniers):
        theta = theta[:-1]

    r = dict()
    r["denier"]      = deniers
    r["yarn_radius"] = yarn_radius
    r["height"]      = hs
    r["theta"]       = theta
    r["radius_max"]  = radius_max
    r["denier_per_new"] = denier_per_new
    r["pressure"]   = pressure
    return r