
from tools.step.common import common



def default():
    p = common()
    p["young"]   = 2960 # MPa
    p["poisson"] = 0.37 # 
    p["epsilon"] = 0.1 # [-] strain
    p["OMP_NUM_THREADS"] = 4 # number of cpus
    p["type_bc"] = 3 # 1: fixed bot x y z , fixed z top, 2:
    p["attemps"] = 4 # number of attemps
    p["Adjust"] = False #  calculix adjust parameter
    p["nfixed"] = 3 # number of fixed nodes in the bottom
    p["nsteps"] = 2 # number of steps
    p["nonlinear"] = False # nonlinear simulation
    p["cylindrical"] = False # cylindrical simulation
    p["nruns"] = 1
    p["surface_interaction"] = dict()
    p["surface_interaction"]["type"] = "hard" # "hard" or "exponential"
    p["surface_interaction"]["factor_E"] = 50 # times E young modulus
    p["max_mono"] = None # MPa
    p["calculix_dynamic"] = False # dynamic simulation
    p["mpi"] = False # dynamic simulation
    p["mpi_np"] = 4 # dynamic simulation
    p["inflation_path"] = ""
    return p