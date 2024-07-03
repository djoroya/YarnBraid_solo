from matplotlib import pyplot as plt
import numpy as np
def plot_lambda_d(r,last=False):
    theta          = r["theta"]
    radius_max     = r["radius_max"]
    denier_per_new = r["denier_per_new"]
    pressure       = r["pressure"]
    fontsize = 11
    # fonttimes = "Times New Roman"
    font = "Serif"
    # default
    plt.rcParams['font.family'] = font
    # padding
    plt.subplots_adjust(hspace=0.6)
    plt.subplot(3,1,1)

    plt.plot(np.array(theta)*(180/np.pi),denier_per_new,
             "o-",label="Sim | [" +str(round(pressure[0]))+r" MPa]") 
    if last:
        plt.xlabel(r"$\theta (deg)$")
        plt.ylabel(r"$\lambda \ (denier)$",fontsize=fontsize)
        plt.title("Linear density",fontsize=fontsize)

        denier_exp = 540 
        xlims = plt.xlim()
        plt.plot([0,90],[denier_exp,denier_exp],"--",color="black",label="Experimental")
        plt.xlim(xlims)
    plt.legend(loc="upper right",bbox_to_anchor=(1.5,1))

    plt.grid()
    # y left axis
    # =====================
    plt.subplot(3,1,2)
    plt.plot(np.array(theta)*(180/np.pi),
             2*np.array(radius_max),
            "o-",
            label="Sim | [" +str(round(pressure[0]))+r" MPa]")

    if last:
        diameter = 4
        xlims = plt.xlim()
        plt.plot([0,90],[diameter,diameter],
                "--",
                color="black",
                label="Experimental")
        plt.xlim(xlims)
        plt.title("Diameter",fontsize=fontsize)
        plt.ylabel("d (mm)",fontsize=fontsize)
        # outside box
        plt.grid()
        plt.xlabel(r"$\theta (deg)$")
    plt.legend(loc="upper right",bbox_to_anchor=(1.5,1))

    plt.subplot(3,1,3)
    plt.plot(2*np.array(radius_max),denier_per_new,
             "o-",
             label="Sim | [" +str(round(pressure[0]))+r" MPa]")
    if last:
        plt.plot(diameter,denier_exp,"o",
                color="black",label="Experimental")
        xlims = plt.xlim()

        plt.plot([0,6],[denier_exp,denier_exp],"--",color="black")
        plt.xlim(xlims)
        ylim = plt.ylim()
        plt.plot([diameter,diameter],[0,ylim[1]],"--",color="black")
        plt.ylim(ylim)
        plt.xlabel(r"$d (mm)$")
        plt.ylabel(r"$\lambda \ (denier)$",fontsize=fontsize)
        plt.grid()
    plt.legend(loc="upper right",bbox_to_anchor=(1.5,1))

    # text theta
    for i in range(len(theta)):
        text = r"$\theta = "+str(round(theta[i]*(180/np.pi)))+r"^\circ$"
        plt.text(2*radius_max[i],denier_per_new[i],
                text,fontsize=9)