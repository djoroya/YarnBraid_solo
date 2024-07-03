from matplotlib import pyplot as plt
from model.post.plot_esq import plot_esq
import numpy as np

def plot_yarns(results,df_params,limits=None):

    nresults = len(results)
    nsq = int(np.sqrt(nresults)) + 1
    # current figure
    fig = plt.gcf()
    for i in range(nsq):
        for j in range(nsq):
            step = i*nsq+j
            if step >= nresults:
                break
            #h = df_params.iloc[step]["h"]
            #r = df_params.iloc[step]["r"]
            #label = "h={:.2f}, r={:.2f}".format(h,r)
            label=""
            ax = fig.add_subplot(nsq,nsq,step+1, projection='3d')
            if results[step] is not None:
                plot_esq(results[step])

                # xlim 
                if limits is not None:
                    ax.set_xlim3d(limits["x"][0],limits["x"][1])
                    ax.set_ylim3d(limits["y"][0],limits["y"][1])
                    ax.set_zlim3d(limits["z"][0],limits["z"][1])
                else:
                    ax.set_xlim3d(-5,5)
                    ax.set_ylim3d(-5,5)
                    ax.set_zlim3d(-12,2)
                # aspect ratio
                ax.set_aspect('equal')
                # axis off
                ax.set_axis_off()
                #plt.title(label)
                # tight layout
                plt.tight_layout()
            else:
                print("No results for step {}".format(step))
                ax.set_axis_off()

