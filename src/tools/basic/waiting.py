import time
import datetime
from tqdm.auto import tqdm
from tools.basic.loadsavejson import loadjson
MaxTime = 4 # hours
dt = 5 # minutes

def waiting(json_file,MaxTime, dt,fcn_wait):
    Nsteps = int(MaxTime*60/dt)
    print("Waiting for", MaxTime, "hours")
    print("Nsteps =", Nsteps)
    print("dt =", dt, "minutes")
    print(10*"-")
    for i in tqdm(range(Nsteps)):
        params_json = loadjson(json_file)
        if fcn_wait(params_json):
            print("Done!")
            break
        else:
            print("Waiting ...")
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(dt*60)
