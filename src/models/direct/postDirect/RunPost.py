from tools.calculix.frd.readfrd import readfrd
from models.direct.postDirect.interp_section import interp_section
import os
import numpy as np
import glob
from tools.step.runstep import runstep,address,lj
from settings.simulations import simulations

join = os.path.join
@runstep(address(__file__))
def RunPost(params,outfolder):

    sim_path        = params["tensile_path"]
    verbose         = params["settings_step"]["verbose"]

    def printv(*args,**kwargs):
        if verbose:
            print(*args,**kwargs)

    simu_params = lj(sim_path)
    infl_path   = simu_params["inflation_path"]
    infl_params = lj(infl_path)
    nsets       = infl_params["nsets"]
    # si r_hebra no esta en simu_params, lo agregamos
    simu_params["r_hebra"] =  infl_params["r_hebra"]
    #

    printv("Read frd\n" + "-"*20)	
    frd = readfrd(join(simulations(),sim_path,"init_new.frd"))
    
    frds_path = join(simulations(),sim_path,"init_new_*.frd")
    frds_path = glob.glob(frds_path)
    frds_path.sort()
    if len(frds_path) > 0:
        #frd_add = [ readfrd(ifrd) for ifrd in frds_path]  
        frd_add = []
        for ifrd_path in frds_path:
            try:
                frd_add.append(readfrd(ifrd_path))
            except:
                printv("Error reading frd file: " + ifrd_path)
        #
        if len(frd_add) > 0:

            data_blocks = [ ifrd["data_blocks"] for ifrd in frd_add]
            data_sum = []
            for ifrd in frd_add:
                data_sum = data_sum + ifrd["data_blocks"]
            data_blocks = data_sum
            frd["data_blocks"] = frd["data_blocks"] + data_blocks
            frd["data"] = frd["data_blocks"][-1]
            steps = [ ifrd["steps"] for ifrd in frd_add]
            steps = np.concatenate([*steps])
            # add in frd["steps"]
            frd["steps"] = np.concatenate([frd["steps"],steps])

    printv("Interp section\n" + "-"*20)


    TOP = [ nsets[iname] for iname in nsets.keys() if "TOP" in iname]
    BOT = [ nsets[iname] for iname in nsets.keys() if "BOT" in iname]
    def getL(var,ifrd):
        TOP_pos = [ np.mean(ifrd.loc[iTOP][[var]].values,axis=0) 
                for iTOP in TOP]
        TOP_pos_mean = np.mean(TOP_pos)
        BOT_pos = [ np.mean(ifrd.loc[iBOT][[var]].values,axis=0)
                    for iBOT in BOT]
        BOT_pos_mean = np.mean(BOT_pos)

        return TOP_pos_mean - BOT_pos_mean 
    
    measurements = []

    for ifrd in frd["data_blocks"]:

        yarns = interp_section(ifrd,nsets,ndisk=20)

        mt = [ [ idisk["mean"]  for idisk in iyarn["disks"]]  
            for iyarn in yarns]
        mt = np.array(mt)
        mt_z = [ [ idisk["center"][2]  
                for idisk in iyarn["disks"]]  
                for iyarn in yarns]
        
        mt_z      = np.array(mt_z)
        nz = len(mt_z[0])
        id_init = int(0.15*nz)
        id_end = int(0.85*nz)
        sigma_max = np.max(mt[:,id_init:id_end])
        
        z_mu    = np.mean(ifrd["z"])
        F_total = np.sum(ifrd["F3"][ifrd["z"]>z_mu])

        # ==========
        ifrd["zD"] = ifrd["z"] + ifrd["D3"]
        L_original = getL("z",ifrd)
        Delta_L = (getL("zD",ifrd) - L_original)
        epsilon = Delta_L/L_original
        # ==========

        bol_z = ifrd["z"]>z_mu
        bol_alma = (ifrd["x"]**2 + ifrd["y"]**2) < 0.8**2
        Falma = np.sum((ifrd["F3"][bol_z & bol_alma]))
        Ftrenzado = F_total - Falma
        # ==========
        r = dict()

        #r["yarns"]          = yarns
        r["sigma_max"]      = sigma_max
        r["F_total"]        = F_total
        r["Ftrenzado"]      = Ftrenzado
        r["Falma"]          = Falma
        r["Delta_L"]        = Delta_L
        r["mt"]             = mt
        r["mt_z"]           = mt_z
        r["length"]         = np.max(mt_z) - np.min(mt_z)
        r["epsilon"]        = epsilon
        measurements.append(r)
    
    frd_dict = dict()
    frd_dict["steps"] = frd["steps"]
    #
    infl_params_dict = dict()
    infl_params_dict["pressure"] = infl_params["pressure"]
    infl_params_dict["simulation_path"] = infl_params["simulation_path"]

    simu_params_dict = dict()
    simu_params_dict["nonlinear"] = simu_params["nonlinear"]
    # 
  
        
    results = {

        "measurements":measurements,
        "frd":frd_dict,
        "infl_params":infl_params_dict,
        "simu_params":simu_params_dict,
    }

    params["results"] = results

    return params