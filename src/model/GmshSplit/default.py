from tools.step.common import common

def default():
    p = common()
    p["factor_radius"] = 0.8
    p["factor_mesh_min"] = 2.3
    p["factor_mesh_max"] = 2.8
    p["debug"] = False
    p["refine"] = False
    p["lammps_path"] = ""

    return p
