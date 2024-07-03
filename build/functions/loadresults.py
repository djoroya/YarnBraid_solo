from tools.basic.loadsavejson import loadjson
import os

join = os.path.join
lj = lambda *args: loadjson(join(*args))

def loadresults(paths):

    results = []
    good_paths = []
    for i,path in enumerate(paths):
        try:
            results.append(lj(path,"post","params.json"))
            lmp = lj(path,"lammps","params.json")
            results[-1]["lammps"] = lmp
            good_paths.append(i)
        except Exception as e:
            print("problem with", path, e)
            pass
        
    L           = [ r["L"]/4*(65/60) for r in results]

    # sort by L
    arg = sorted(range(len(L)), key=lambda k: L[k])
    results = [ results[i] for i in arg]
    good_paths = [ good_paths[i] for i in arg]
    # sort by L
   
    size_square = [ r["lammps"]["size_square"] for r in results]
    ratio       = [ r["ratio"] for r in results]
    A           = [ r["A"] for r in results]
    L           = [ r["L"]/4*(65/60) for r in results]
    sigma_max   = [ r["sigma_max"] for r in results]
    sigma_apl   = [ r["sigma_apl"] for r in results]
    F_apl       = [ r["F_apl"] for r in results]

    ms = {
        "results": results,
        "size_square": size_square,
        "ratio": ratio,
        "sigma_max": sigma_max,
        "sigma_apl": sigma_apl,
        "F_apl": F_apl,
        "A": A,
        "L": L,
    }
    

    return ms, good_paths