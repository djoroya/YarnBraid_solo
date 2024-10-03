# read dump.xyz
import numpy as np
#read lines
import os
from models.direct.lammpshard.traj2df   import traj2df
from models.direct.lammpshard.smooth_trajectory_fourier import smooth_trajectory_fourier
import pandas as pd

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



  
    all_bonds = params["all_bonds"] 

    # tenemos que añadir los enlaces entre los hilos
    len_periodic = 1/8
    to_horario = int(64*len_periodic/2) + 1
    to_antiho  = int(64*len_periodic/2) + 33

    horario = np.arange(1,to_horario,1)     
    antiho  = np.arange(33,to_antiho,1)
        
    merge = np.concatenate((horario,antiho),axis=0)
    all_bonds = []
    for i in merge:
        bonds = [ i + int(64*len_periodic/2)*j 
                 for j in range(int(1/len_periodic))]

        pairs = [ [bonds[j], bonds[j+1]] for j in range(len(bonds)-1)]
        pairs.append([bonds[-1], bonds[0]])
        all_bonds.append(bonds)


    trajs_index = []
    for k in range(8):
        for i in range(4):
            start = k 
            end   = np.mod(k+7,8) 

            if start >= end:
                part1 = all_bonds[i][start:]
                part2 = all_bonds[i][:end+1]
                part1.extend(part2)
            else:
                part1 = all_bonds[i][start:end+1]
            print(part1)
            trajs_index.append(part1)

    for k in range(8):
        for i in range(4):
            start = k 
            end   = np.mod(k+7,8) 

            if start >= end:
                part1 = all_bonds[i+4][start:]
                part2 = all_bonds[i+4][:end+1]
                part1.extend(part2)
            else:
                part1 = all_bonds[i+4][start:end+1]
            print(part1)
            trajs_index.append(part1)            
            # print("start",start)
            # print("end",end)
            
    h = params["h"]

    merge_trajs = [ [ trajs[i-1].copy() + np.array([0,0,j*h/8])
                     for j,i in enumerate(itindx)] for itindx in trajs_index]
    merge_trajs = [ np.concatenate(traj,axis=0) for traj in merge_trajs]

    trajs = merge_trajs

    if not params["only_small"]:
        for bond in all_bonds:
            itraj = trajs[bond[0]-1]
            points_to_add = trajs[bond[1]-1][0].copy()
            points_to_add[2] += h*params["len_periodic"]

            trajs[bond[0]-1] = np.concatenate([itraj,points_to_add[None,:]],axis=0)
            #

            penultimate_point = trajs[bond[0]-1][-2].copy()
            second_point      = trajs[bond[1]-1][1].copy()
            second_point[2] += h*params["len_periodic"]

            rmu = 0.5*(penultimate_point + second_point)

            trajs[bond[0]-1][-1] = rmu.copy()
            rmu[2] -= h*params["len_periodic"]
        trajs[bond[1]-1][0] = rmu.copy()

        # trajs[bond[0]-1][1] = new_second_point

    trajs = [ smooth_trajectory_fourier(traj) for traj in trajs ]



    params["df"] = traj2df(trajs)

    dfs = [ df[df["type"]==i] for i in range(1,len(df["type"].unique())+1) ]
    t1 = dfs[0].values[:,1:]
    t2 = dfs[1].values[:,1:]
    #compute the minimum distance between the two yarns
    r0 = np.min(np.linalg.norm(t1[:,None,:]-t2[None,:,:],axis=-1))/2
    params["radius"] = r0





    return params