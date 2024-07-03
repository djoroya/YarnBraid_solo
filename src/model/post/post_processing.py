from  tools.basic.loadsavejson import loadjson,savejson
from tools.calculix.frd.readfrd import readfrd
from model.post.interp_section import interp_section
import os
import numpy as np
import glob

def post_processing(sim_path,verbose=True,force_recompute=False,max_mono=None):

    def printv(*args,**kwargs):
        if verbose:
            print(*args,**kwargs)

    post_path    = os.path.join(sim_path,"post_processing")
    results_path = os.path.join(post_path,"results.json")
    if not force_recompute:
        if os.path.exists(results_path):
            try:
                return loadjson(results_path)
            except:
                printv("Error loading results, recompute")
                pass
    # =================
    simu_params = loadjson(os.path.join(sim_path ,"params.json"))
    infl_path   = simu_params["inflation_path"]
    infl_params = loadjson(infl_path + "/params.json")
    nsets       = infl_params["nsets"]
    # si r_hebra no esta en simu_params, lo agregamos
    simu_params["r_hebra"] =  infl_params["r_hebra"]
    #
    # =================
    # lsdyna params 
    try:
        gmsh_path = os.path.join(infl_params["root_folder"],
                                infl_params["gmsh_path"])
        #
        # C02_YarnBraid/validation/ -> C02_YarnBraid/T04_validation/
        gmsh_path = gmsh_path.replace("C02_YarnBraid/validation/",
                                        "C02_YarnBraid/T04_validation/")
        #
        gmsh_params = loadjson(gmsh_path + "/params.json")

        lsdyna_path = os.path.join(gmsh_params["root_folder"],
                                    gmsh_params["lsdyna_path"])
        
        lsdyna_path = lsdyna_path.replace("C02_YarnBraid/validation/",
                                        "C02_YarnBraid/T04_validation/") 
        lsdyna_params = loadjson(lsdyna_path + "/params.json")
    except:
        lsdyna_params = dict()
        lsdyna_params["factor_npoints"] = -1

        
    # =================


    printv("Read frd\n" + "-"*20)	
    frd = readfrd(os.path.join(sim_path,"init_new.frd"))
    
    frds_path = os.path.join(sim_path,"init_new_*.frd")
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


        # compute area total projection z axis
        def getproj(yarn):
            vec = yarn["dr"][-1]
            vec = 1*vec/np.linalg.norm(vec)
            r = np.sqrt(vec[0]**2 + vec[1]**2)
            theta = -np.arctan2(vec[2],r)

            return np.cos(theta)
        
        r = simu_params["r_hebra"]
        A = [np.pi*r**2*getproj(iyarn) for iyarn in yarns]
        A_total = np.sum(A)

        z_mu    = np.mean(ifrd["z"])
        F_total = np.sum(ifrd["F3"][ifrd["z"]>z_mu])

        sigma = F_total/A_total
        # ==========
        ifrd["zD"] = ifrd["z"] + ifrd["D3"]
        L_original = getL("z",ifrd)
        Delta_L = (getL("zD",ifrd) - L_original)
        epsilon = Delta_L/L_original
        # ==========

        # Compute ratio

        N_cen = 15
        r_cen = 0.27/2
        A_cen = np.pi*r_cen**2*N_cen

        A_tren  = A_total
        A_total = A_cen + A_tren

        F_tren = F_total*A_tren/A_total

        sigma_tren = F_tren/A_tren
        new_ratio = sigma_tren/sigma_max


        # ==========
        r = dict()

        #r["yarns"]          = yarns
        r["sigma_max"]      = sigma_max
        r["A_total"]        = A_total
        r["F_total"]        = F_total
        r["sigma"]          = sigma
        r["sigma_tren"]     = sigma_tren
        r["Delta_L"]        = Delta_L
        r["mt"]             = mt
        r["mt_z"]           = mt_z
        r["ratio"]          = sigma/sigma_max
        r["ratio_new"]      = new_ratio
        r["length"]         = np.max(mt_z) - np.min(mt_z)
        r["epsilon"]        = epsilon
        r["young_aprox"]    = sigma/epsilon
        measurements.append(r)
    
    frd_dict = dict()
    frd_dict["steps"] = frd["steps"]
    #
    infl_params_dict = dict()
    infl_params_dict["pressure"] = infl_params["pressure"]
    infl_params_dict["output_folder"] = infl_params["output_folder"]
    infl_params_dict["denier_per_filament"] = infl_params["denier_per_filament"]
    infl_params_dict["theta"] = infl_params["theta"]
    infl_params_dict["height"] = infl_params["height"]
    # 
    simu_params_dict = dict()
    simu_params_dict["nonlinear"] = simu_params["nonlinear"]
    # 
    lsdyna_params_dict = dict()
    lsdyna_params_dict["factor_npoints"] = lsdyna_params["factor_npoints"]

    if max_mono is not None:
        
        step_str =  [ i[:7 ] for i in frd_dict["steps"] ]
        step_str = np.array(step_str)    
        step_str_uq = np.unique(step_str)

        indx = [ np.where(step_str == iuq )[-1][-1] for iuq in step_str_uq]

        ms_select = [ measurements[i] for i in indx]
        sigma_max =  [ r["sigma_max"]  for r in ms_select]
        sigma    =  [ r["sigma"]  for r in ms_select]
        # find index max_mono similar to sigma_max
        dist = np.abs(np.array(sigma_max) - max_mono)
        indx = np.argmin(dist)  

        best_ratio = ms_select[indx]["ratio_new"]
        best_sigma = sigma[indx]
        best_sigma_max = sigma_max[indx]
        ind_ms     = indx
    else:
        best_ratio = None
        ind_ms     = None
        best_sigma = None
        best_sigma_max = None
        
        
    results = {

        "measurements":measurements,
        "frd":frd_dict,
        "infl_params":infl_params_dict,
        "simu_params":simu_params_dict,
        "lsdyna_params":lsdyna_params_dict,
        "ratio":best_ratio,
        "sigma":best_sigma,
        "ind_ms":ind_ms,
        "sigma_max":best_sigma_max
    }

    # create a folder post_processing in sim_path
    if not os.path.exists(post_path):
        os.mkdir(post_path)

    # save results
    savejson(results,results_path)
    


    return results