
from tools.step.common import common,stepsettings
from models.direct.lammpshard.default import default as lmp_default
from models.direct.GmshSplit.default import default as defaultGmshSplit
from models.direct.InflationDirect.default import default as inflation_direct_default

from model.simulation.default import default as simulation_default
from models.direct.postDirect.default import default as post_default

def default():
    p = stepsettings()
    p["has_children"] = True
    p["lammps_sim"]  = lmp_default()
    p["gmsh"]        = defaultGmshSplit()
    p["inflation"]   = inflation_direct_default()
    p["simulation"]  = simulation_default()
    p["post"]        = post_default()
    p["only_lammps"] = False
    return p

