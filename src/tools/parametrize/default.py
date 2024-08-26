from tools.step.common import stepsettings

def default():
    p = stepsettings()
    p["module"]  = "" # Name of the module
    p["function_module"]     = ""
    p["vars"]       = {}
    p["default"]   = {}
    return p