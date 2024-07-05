from tools.step.common import common    

def default():
    p = common()
    p["tensile_path"]        = ""
    p["max_mono"] = None

    return p
