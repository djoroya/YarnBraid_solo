
from tools.step.common import common
import numpy as np



def gmsh_default_table():
    p = common()
    p["factor_radius"] = 0.8
    p["factor_mesh_min"] = 2.3
    p["factor_mesh_max"] = 2.8
    p["debug"] = False
    p["refine"] = False

    return p

def lmp_default():
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

def lsdyna_default():
    p = common()
    p["radius"]        = None
    p["factor_npoints"] = 1/8
    p["align"]         = False
    p["factor"]        = 0.9
    p["hmax"]          = None
    return p

def gmsh_default():
    p = common()
    p["size_element"]  = None # If is None, size ele,ent take radius of yarn 1.2
    p["Algorithm"]     = 1
    p["factor"]        = None # If is None, size ele,ent take radius of yarn 1.2
    return p

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
    p["lammps"]      = lmp_default()
    p["lsdyna"]      = lsdyna_default()
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