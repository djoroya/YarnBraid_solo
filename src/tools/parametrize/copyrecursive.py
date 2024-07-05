def copyrecursive(a):
    if isinstance(a,dict):
        return {k:copyrecursive(v) for k,v in a.items()}
    return a