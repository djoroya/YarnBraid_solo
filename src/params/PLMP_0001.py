from model.default import lmp_default
import numpy as np

def PLMP_0001():
    params = lmp_default()

    params["hilo_central"]    = 40
    params["errate"]          = 0
    params["Npoints"]          = 250
    params["RUN_STEPS_DEFORM"] = 1000
    params["RUN_STEPS_EQ"]     = 1
    params["errate"]  = 0
    params["nhilos"]  = 4 
    params["r_hebra"] = 0.27/2 # mm
    params["theta"]   = 65*(np.pi/180) # deg
    params["dist_factor"] = 1.1
    params["r0_factor"]   = 0.0005
    params["yukawa"]["A"] = 6e3
    params["Remesh"] = False
    params["V0_bond"] = 2e5
    return params