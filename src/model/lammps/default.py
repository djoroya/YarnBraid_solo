import numpy as np
from tools.step.common import common

def default():
    p = common()
    p["Npoints"]       = 150
    p["hilo_central"]  = 0
    p["theta"] = np.deg2rad(51)
    p["factor"]        = 4
    p["Remesh"]        = False
    p["RUN_STEPS_EQ"]     = 1
    p["RUN_STEPS_DEFORM"]   = 10000
    p["errate"]  = 0
    p["nhilos"]  = 4
    p["dist_factor"] = 1.2
    p["r0_factor"] = 0.25
    p["V0_bond"] = 300
    p["r_hebra"] = 0.2
    p["external_hilos"] = False
    p["recompute_dist"] = False
    p["recompute_factor"] = 1
    p["Npoints_density"] = None # 

    # ======================================================
    p["yukawa"] = dict()
    p["yukawa"]["A"] =  500.0
    p["yukawa"]["kappa"] = 1.0
    p["yukawa"]["cutoff"] = None
    #
    p["OMP_NUM_THREADS"] = 1
    p["mpi"] = False
    p["mpi_np"] = 4

    return p