from matplotlib import pyplot as plt
def plot_interp_section(iyarn,ax):
    xvalues = iyarn["x"]
    yvalues = iyarn["y"]
    zvalues = iyarn["z"]
    fvalues = iyarn["f"]
    disks   = iyarn["disks"]

    ax.scatter(xvalues, 
               yvalues, 
               zvalues, 
               c=fvalues,
            cmap='viridis', linewidth=0.5,marker=".",s=0.2)

    for i in range(len(disks)):
        # norm
        f = disks[i]["values"]
        X_trans = disks[i]["X"]
        Y_trans = disks[i]["Y"]
        Z_trans = disks[i]["Z"]

        ax.scatter(X_trans.flatten(),
                   Y_trans.flatten(),
                   Z_trans.flatten(),
                   c = f.flatten())
        translate = disks[i]["center"]
        plt.plot(translate[0],translate[1],translate[2],"ok")
        # aspec ratio
    # 
    ax.set_aspect('equal')
