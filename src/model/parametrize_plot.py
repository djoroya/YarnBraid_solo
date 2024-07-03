
from matplotlib import pyplot as plt
# colors 
from matplotlib import cm
import numpy as np

def parametrize_plot(vars_json,frds,inflation_params,df,zlim=[-15,15],nplots=10):
    
    esq = [[ inf_params["nsets"]["esqueleto_"+str(i)] 
       for i in range(1,65)]
       for inf_params in inflation_params]
    
    colors = cm.rainbow(np.linspace(0, 1, 64))

    nplots = np.min([len(frds),nplots])
    nsq = np.sqrt(nplots)
    nsq = int(nsq) +1 

    names = vars_json["df"].columns.values
    for i in range(nsq):
        for j in range(nsq):

            if i*nsq+j >= nplots:
                break

            frd = frds[i*nsq+j]
            if frd is None:
                continue
            
            plt.subplot(nsq, nsq, i*nsq+j+1, projection='3d')
        
            for k in range(64):
                esq_1 = esq[i*nsq+j][k]
                x = frd["data"].loc[esq_1]["x"]
                y = frd["data"].loc[esq_1]["y"]
                z = frd["data"].loc[esq_1]["z"]

                vars_value = [ df[ivar].values[i*nsq+j] 
                              for ivar in names ]
                # 3d 
                plt.plot(x.values, y.values, z.values,
                        color=colors[k],
                        marker=".", 
                        linestyle='None',
                        ms=1)
            plt.axis('equal')
            plt.xlim(-15, 15)
            plt.ylim(-15, 15)
            plt.gca().set_zlim(zlim[0], zlim[1])
            title = [ str(names[i]) + " = {:.2f}".format(vars_value[i]) for i in range(len(names)) ]
            plt.title(" --- ".join(title))