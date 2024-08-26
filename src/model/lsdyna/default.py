from tools.step.common import stepsettings    

def default():
    p = stepsettings()
    p["radius"]        = None
    p["factor_npoints"] = 1/8
    p["align"]         = False
    p["factor"]        = 0.9
    p["hmax"]          = None
    p["npoints"]       = 50
    p["lmp_path"]      = ""
    return p
