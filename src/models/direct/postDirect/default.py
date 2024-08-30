from tools.step.common import stepsettings    

def default():
    p = stepsettings()
    p["tensile_path"]        = ""
    p["max_mono"] = None

    return p
