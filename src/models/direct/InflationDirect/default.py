
from tools.step.common import stepsettings

def default():
    p = stepsettings()
    p["pressure"]  = 300 # Pa
    p["OMP_NUM_THREADS"]     = 16
    p["attemps"] = 4 # number of attemps

    p["surface_behavior"] = dict()
    p["surface_behavior"]["type"] = "hard" # "hard" or "exponential"
    p["surface_behavior"]["dist"] = 0.1 # mm
    p["surface_behavior"]["pressure"] = 1000 # Pa
    p["radius_target"] = 10 # mm
    p["rho"] = 0.00097 # g/mm^3
    p["calculix_dynamic"] = False # dynamic simulation
    p["mpi"] = False # dynamic simulation
    p["mpi_np"] = 4 # dynamic simulation
    p["nsteps"] = 1 # number of steps
    p["nlgeom"] = True # nonlinear simulation
    p["gmsh_path"] = ""
    p["auto_pressure"] = False
    p["ties_activate"] = False
    return p
