from tools.step.common import common

def default():
    p = common()
    p["size_element"]  = None # If is None, size ele,ent take radius of yarn 1.2
    p["Algorithm"]     = 1
    p["factor"]        = None # If is None, size ele,ent take radius of yarn 1.2
    p["lsdyna_path"]   = ""
    return p