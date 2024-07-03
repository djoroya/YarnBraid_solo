from matplotlib import pyplot as plt
import numpy as np

def evolutions(results):

    n_results = len(results["measurements"])
    fig = plt.figure(figsize=(8,8))
    # padding 
    plt.subplots_adjust(wspace=0.5,hspace=0.5)
    nsq = int(np.ceil(np.sqrt(n_results)))
    if nsq**2 < n_results:
        nsq += 1
    max_sigma = np.max([np.max(r["mt"]) for r in results["measurements"]])

    for j,r in enumerate(results["measurements"]):
        plt.subplot(nsq,nsq,j+1)
        yarns = r["yarns"]
        mt,mt_z = r["mt"],r["mt_z"]
        for iyarn in range(len(yarns)):
            z = mt_z[iyarn]
            plt.plot(z,mt[iyarn,:],'.-')
        plt.xlabel("z [mm]")
        plt.ylabel("Mean Disk stress (P1)[MPa]")
        plt.ylim([0,200])
        plt.title(results["frd"]["steps"][j])
        plt.ylim([0,max_sigma])

        
        plt.grid()


def sigmas(results,name=""):

    epsilons = [ r["epsilon"] for r in results["measurements"]]
    F_total  = [ r["F_total"] for r in results["measurements"]]
    ratio    = [ r["ratio"] for r in results["measurements"]]
    sigma_max= [ r["sigma_max"] for r in results["measurements"]]

    # ==============================================
    plt.subplot(3,1,1)
    plt.plot(epsilons,ratio,
             label=name,
             marker="o")
    
    plt.xlabel("$\epsilon$")
    plt.ylabel("ratio")

    plt.legend()
    plt.grid()
    # ==============================================
    plt.subplot(3,1,2)

    plt.plot(epsilons,sigma_max,
             label="sigma_max" + " " + name,
             marker="o")
    
    plt.xlabel("$\epsilon$")
    plt.ylabel("$\sigma_{max}$  [MPa]")

    plt.legend()
    plt.grid()
    # ==============================================

    plt.subplot(3,1,3)

    plt.plot(epsilons,F_total,label="$F_{total}$" + " " + name,marker="o")

    plt.xlabel("$\epsilon$")
    plt.ylabel("$F_apl$  [N]")

    plt.legend()
    plt.grid()



def strain_stress(results_exp_mono,results_exp,results):


    df_mono = results_exp_mono["df_exp"]["exp 1"]
    epsilons  =  [ r["epsilon"]   for r in results["measurements"]]
    sigma     =  [ r["sigma"]     for r in results["measurements"]]
    sigma_max =  [ r["sigma_max"] for r in results["measurements"]]
    # ==============================================
    plt.plot(epsilons,sigma,label="$\sigma_{apl}$",marker="o")
    plt.plot(epsilons,sigma_max,label="$\sigma_{max}$",marker="o")

    plt.xlabel(r"$\epsilon$")
    plt.ylabel(r"$\sigma_{apl} \ [MPa]$")
    steps = results["frd"]["steps"]

    for i in range(len(steps)):
        text_text = steps[i].split("_")
        text_text = "$s_{"+str(text_text[1])+"}"+"^{"+str(text_text[2])+"}$"
        plt.text(epsilons[i],sigma[i],
                 text_text,rotation=0,ha="center",va="center")
        plt.text(epsilons[i],sigma_max[i],text_text,
                 rotation=0,ha="center",va="center")

    plt.plot(results_exp["df_exp_1"]["strain [-]"],
             results_exp["df_exp_1"]["stress [MPa]"],
            label="Trenzado Exp. 1",ls="--")


    # plot df_mono
    plt.plot(df_mono["strain [-]"],
             df_mono["stress [MPa]"],
            label="Mono Exp. 1",ls="--")

    ratio     = results["measurements"][-1]["ratio"]
    new_ratio = results["measurements"][-1]["ratio_new"]
    title = "Ratio: "+str(round(ratio,2)) + " | Ratio (Corrected): "+str(round(new_ratio,2))
    plt.title(title)
    plt.grid()
    plt.xlim(0,0.2)
    plt.ylim(0,50)
    plt.legend()