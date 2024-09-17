import numpy as np
def createalma(Nhilos,zmin,zmax,Npoints = 100):

    # basis hexagonal 

    d = 0.27/2
    a = [1,0]
    b = [1/2,np.sqrt(3)/2]
    a = np.array(a)*d*2
    b = np.array(b)*d*2


    Na = 40
    Nb = 40

    points = []
    for i in range(Na):
        for j in range(Nb):
            points.append([i*a[0] + j*b[0],i*a[1] + j*b[1]])

    points = np.array(points) 

    rmu = points.mean(axis=0)
    ## search for the closest point
    rmu_dist = np.linalg.norm(points-rmu,axis=1)
    rmu = points[np.argmin(rmu_dist)]

    points = points - rmu
    rmu = rmu - rmu
    distances = []
    for i in range(len(points)):
            distances.append(np.linalg.norm(points[i]-rmu))

    distances = np.array(distances)

    # sort points by distance
    points = points[distances.argsort()]

    points = points[:Nhilos]


    zspan = np.linspace(zmin,zmax,Npoints)
    trajs = []

    for i in range(len(points)):
        r0 = points[i]
        # create [x0,y0,z_i] for each point
        traj = np.zeros((Npoints,3))
        traj[:,0] = r0[0]
        traj[:,1] = r0[1]
        traj[:,2] = zspan   
        trajs.append(traj)


    return trajs