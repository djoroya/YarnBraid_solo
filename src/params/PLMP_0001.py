from model.default import lmp_default

def PLMP_0001():
    params = lmp_default()

    params["Npoints"] = 250
    params["RUN_STEPS_DEFORM"] = 25000
    params["RUN_STEPS_EQ"]     = 1
    params["errate"]  = 0
    params["nhilos"]  = 4
    params["r_hilo"] = 15
    params["h"] =50
    params["dist_factor"] = 0.2
    params["r0_factor"] = 0.0005
    params["yukawa"]["A"] = 500
    params["yukawa"]["kappa"] = 0.1
    params["hilo_central"] = 10
    params["Remesh"] = False
    params["remove_final"] = True

    params["V0_bond"] = 38000
    params["OMP_NUM_THREADS"] = 4
    params["mpi"] = True
    return params