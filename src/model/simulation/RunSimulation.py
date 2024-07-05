import os
from tools.basic.loadsavejson     import savejson
from tools.step.runstep          import runstep,address
from model.simulation.build_inp import build_inp
from tools.calculix.runccx import runccx
from tools.calculix.read_dat import read_dat
import numpy as np
import shutil
from model.post.post_processing import post_processing


join = lambda *args: os.path.join(*args)

@runstep(address(__file__))
def RunSimulation(params,output_folder,callback=None):

    callback(nstep=2) if callback else None

    # ==============================================================================
    
    # Run update de params["output_folder"] so we update the value
    output_folder = params["output_folder"]
    # ==============================================================================

    callback() if callback else None

    params_infl = build_inp(params)
    # ==============================================================================
    # load lines 
            
    json_file = join(output_folder,"params.json")
    savejson(params,json_file)

    # ==============================================================================
    callback() if callback else None

    error,cmd = runccx(output_folder,
                       name_inp="init_new",
                       OMP_NUM_THREADS = params["OMP_NUM_THREADS"],
                        mpi      = params["mpi"],
                        mpi_np   = params["mpi_np"],
                       att=params["attemps"],
                       dynamic=params["calculix_dynamic"])

    if params["nruns"] > 1:
        #copy init_new.rout to init_new_1.rin
        rout = join(output_folder,"init_new.rout")
        shutil.move(rout, rout.replace(".rout","_1.rout"))

        for i in range(2,params["nruns"]+1):
            rout_pre = join(output_folder,"init_new_{}.rout".format(i-1))
            
            rin_curr = join(output_folder,"init_new_{}.rin".format(i))

            shutil.move(rout_pre, rin_curr)

            error,cmd = runccx(output_folder,
                               name_inp = "init_new_{}".format(i),
                               att      = params["attemps"],
                               OMP_NUM_THREADS = params["ncpus"],
                               mpi      = params["mpi"],
                               mpi_np   = params["mpi_np"],
                               outtxt   = "out_{}.txt".format(i),
                               dynamic  = params["calculix_dynamic"])
            
            os.remove(rin_curr)

            if params["max_mono"] is not None:
                    #max_mono = 142.4 # MPa
                results = post_processing(output_folder, 
                                          max_mono =  params["max_mono"])
                sigma_max = results["measurements"][-1]["sigma_max"]
                if sigma_max > params["max_mono"]:
                    print("Simulation {} of {} finished".format(i,params["nruns"]))
                    break
                else:
                    #sigma_max , params["max_mono"]
                    # print 
                        print("Simulation {} of {} finished".format(i,params["nruns"]))
                        print("Sigma_max: {} MPa".format(sigma_max))
                        print("Max_mono: {} MPa".format(params["max_mono"]))
                        print("The max_mono was not reached, the simulation will continue")
                
            # remove 
            
            if error != 0:
                print("Simulation {} of {} finished".format(i,params["nruns"]))
                print("Error: {}".format(error))
                break
                
    # ==============================================================================

    params["frd"]     = join(output_folder,"init_new.frd")
    params["cmd"]     = cmd
    params["nsets"]   = params_infl["nsets"]
    params["r_hebra"] = params_infl["r_hebra"]

    # read out file and if have "*ERROR in e_c3d: nonpositive jacobian" 
    #raise an error
    # ==============================================================================
    file = join(output_folder,"out.txt")
    with open(file,"r") as f:
        lines = f.readlines()
    for line in lines:
        if "*ERROR in e_c3d: nonpositive jacobian" in line:
            raise ValueError("Nonpositive jacobian")
        
    # ==============================================================================
    # compute volume 
    # this info is in the file: output_folder/init_new.dat
    dat = join(output_folder,"init_new.dat")
    data = read_dat(dat)
    df = data[-1]["df"]
    volume = df["volume"].astype(float)
    volume = np.sum(volume)
    params["volume"] = volume
    
    return params