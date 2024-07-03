from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
# colors 
from matplotlib import cm
def plot_df(df,dim3d=True,fig=None):

    dfs = [ df[df['type'] == i] for i in df['type'].unique() ]

    trajs = [ df[['xu','yu','zu']].values for df in dfs]

    jet = cm.get_cmap('jet', len(trajs))
    if fig is None:
        fig = plt.figure()
    if dim3d:
        ax = fig.add_subplot(111, projection='3d')
        for i,traj in enumerate(trajs):
            label = "yarn {}".format(i+1)
            ax.plot(traj[:,0],traj[:,1],traj[:,2],
                    color=jet(i),marker='o',linestyle='-',ms=2,label=label)
    else:
        ax = fig.add_subplot(111)
        for i,traj in enumerate(trajs):
            label = "yarn {}".format(i+1)
            ax.plot(traj[:,0],traj[:,1],color=jet(i),
                    marker='o',linestyle='-',ms=2,label=label)
            # plot init point
            ax.plot(traj[0,0],traj[0,1],color=jet(i),
                    marker='o',linestyle='None',ms=5)
        

    # aspect ratio
    plt.gca().set_aspect('equal', adjustable='box')