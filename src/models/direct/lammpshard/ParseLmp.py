# read dump.xyz
import numpy as np
#read lines
import os
from models.direct.lammpshard.traj2df   import traj2df
import pandas as pd
from models.direct.lammpshard.smooth_trajectory_fourier import smooth_trajectory_fourier

def ParseLmp(params,file):

    dumps_path = os.path.join(params["output_folder"],"dump.xyz")

    lines = open(dumps_path, "r").readlines()

    bol = ["ITEM:" in line for line in lines]
    # find the last true
    idx = np.where(bol)[0][-1]

    lines = lines[idx:]
    lines[0] = lines[0].replace("ITEM: ATOMS ", "")

    # lines to pandas dataframe numeric
    df = pd.DataFrame([line.split() 
                       for line in lines[1:]], 
                       columns=lines[0].split(), 
                       dtype=np.float64)
    #sort by id
    df = df.sort_values(by="id")
    #remove id column
    df = df.drop(columns=["id"])
    #remove mol column
    df = df.drop(columns=["mol"])
    file = os.path.join(params["output_folder"],file)
    df.to_csv(file, index=False)

    params["ParseLmp"] = file

    trajs = [ df[df["type"] == i][["xu","yu","zu"]].values for i in df["type"].unique() ]
    trajs = [ smooth_trajectory_fourier(traj) for traj in trajs ]

    params["df"] = traj2df(trajs)


    params["old_df"] = params["df"].copy()


    params["df"] = traj2df(trajs)

    dfs = [ df[df["type"]==i] for i in range(1,len(df["type"].unique())+1) ]
    t1 = dfs[0].values[:,1:]
    t2 = dfs[1].values[:,1:]
    #compute the minimum distance between the two yarns
    r0 = np.min(np.linalg.norm(t1[:,None,:]-t2[None,:,:],axis=-1))/2
    params["radius"] = r0





    return params