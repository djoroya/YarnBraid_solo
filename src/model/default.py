
from tools.step.common import common,stepsettings
from model.lammps.default import default as lmp_default
from model.lsdyna.default import default as lsdyna_default
from model.Gmsh.default import default as gmsh_default
from model.inflation.default import default as inflation_default
from model.simulation.default import default as simulation_default
from model.post.default import default as post_default

def default():
    p = stepsettings()
    p["has_children"] = True
    p["lammps_sim"]  = lmp_default()
    p["lsdyna_sim"]  = lsdyna_default()
    p["gmsh"]        = gmsh_default()
    p["inflation"]   = inflation_default()
    p["simulation"]  = simulation_default()
    p["post"]        = post_default()
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