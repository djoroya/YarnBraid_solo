def common():
    p = dict()
    p["elapsed"] = 0
    p["error"] = 1
    p["error_msg"] = "No execution"


    return p

def stepsettings():
    p = dict()
    p["has_children"] = False
    p["has_parent"]   = False
    p["verbose"]      = True

    return {"settings_step": p}