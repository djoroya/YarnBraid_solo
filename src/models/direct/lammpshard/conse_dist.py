from tools.basic.loadsavejson import loadjson
import pandas as pd
import numpy as np
import scipy.spatial.distance as dist
import os
def dist_traj(traj1,traj2):
    cdist = dist.cdist(traj1,traj2)
    min = np.min(cdist)
    return min

def conse_dist(lmp_path,nhilos):
    lmp_path = os.path.join(lmp_path,"data.csv")
    trajs = pd.read_csv(lmp_path, sep=",", header=0)
    trajs.index = trajs["type"]
    trajs = trajs.drop(columns=["type"])
    trajs_list = [ trajs.loc[i].values 
                  for i in range(1, 16*nhilos+1) ]
    
    ntrajs = len(trajs_list)
    consecutive_dist = [dist_traj(trajs_list[i],trajs_list[i+1]) 
                        for i in range(0,ntrajs//2)]
    consecutive_dist = np.array(consecutive_dist)

    id =np.arange(nhilos,ntrajs//2,nhilos)-1

    large_dist = np.mean(consecutive_dist[id])
    normal_dist = np.mean(consecutive_dist)

    percent = (large_dist-normal_dist)/normal_dist*100

    r = {"large_dist":large_dist,"normal_dist":normal_dist,"percent":percent,"consecutive_dist":consecutive_dist,"id":id}
    return r
