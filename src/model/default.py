
from tools.step.common import common

def inflation_default():
    p = common()
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
    return p

def simulation_default():
    p = common()
    p["young"]   = 2960 # MPa
    p["poisson"] = 0.37 # 
    p["epsilon"] = 0.1 # [-] strain
    p["OMP_NUM_THREADS"] = 4 # number of cpus
    p["type_bc"] = 3 # 1: fixed bot x y z , fixed z top, 2:
    p["attemps"] = 4 # number of attemps
    p["Adjust"] = False #  calculix adjust parameter
    p["nfixed"] = 3 # number of fixed nodes in the bottom
    p["nsteps"] = 1 # number of steps
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
    return p

def default():
    p = dict()
    p["lammps_sim"]      = lmp_default()
    p["lsdyna_sim"]      = lsdyna_default()
    p["gmsh"]        = gmsh_default()
    p["inflation"]   = inflation_default()
    p["simulation"]  = simulation_default()
    p["only_lammps"] = False
    return p

def traj2mesh_default():
    p = common()
    p["lsdyna_params"]      = lsdyna_default()
    p["gmsh_params"]        = gmsh_default()
    return p

def default_v2():
    p = dict()
    p["lammps"]      = lmp_default()
    p["trajs2mesh"]  = traj2mesh_default()
    p["inflation"]   = inflation_default()
    p["simulation"]  = simulation_default()
    return p