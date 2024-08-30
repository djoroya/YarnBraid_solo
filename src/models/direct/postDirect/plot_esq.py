from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
def plot_esq(results,**kwargs):
    
    frd      = results["frd"]
    json_sim = results["json_sim"]

    nsets = json_sim["nsets"]
    esq = [ nsets["esqueleto_"+str(i)] for i in range(1,65)]

    colors = cm.jet(np.linspace(0, 1, 16))
    # every 4 yarn is a different color
    colors = np.repeat(colors,4,axis=0)
    for i in range(len(esq)):
        
        x = frd["data"].loc[esq[i]]["x"]
        y = frd["data"].loc[esq[i]]["y"]
        z = frd["data"].loc[esq[i]]["z"]

        plt.plot(x,y,z,'.',ms=1,**kwargs,color=colors[i])