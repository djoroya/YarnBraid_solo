from models.direct.lammpshard.curve        import curve
from models.direct.lammpshard.WriteDataLmp import WriteDataLmp 
from models.direct.lammpshard.WriteRunLmp  import WriteRunLmp
from models.direct.lammpshard.ParseLmp     import ParseLmp
import os
from tools.step.runstep import runstep,address
import numpy as np
from tools.lammps.run_lmp import run_lmp
from models.direct.lammpshard.conse_dist import conse_dist
import colorama



def print_header(header):
    print(colorama.Fore.GREEN + header + colorama.Style.RESET_ALL)


@runstep(address(__file__))
def RunLammps(params,output_folder,callback=None):

    callback(nstep=2) if callback else None

    #
    simulation_path = params["output_folder"]

    N     = params["nhilos"]
    rho   = params["r_hebra"]
    theta = params["theta"]
    params["h"] = 16*N*rho/np.sin(np.pi/2 - theta)


    if params["Npoints_density"] is not None:
        params["Npoints"] = int(params["Npoints_density"]*params["h"])
    
    # sin(pi/2 - theta) = cos(theta)
    params["r_hilo"] = params["h"]/(2*np.pi*np.tan(theta))
    # Generate the spiral
    params = curve(params)
    # Write the data file
    if callback is not None:
        print_header("Trajectory Generation")
        print_header("====================================")
    # =======================================================
    # Write the data file
    file   = os.path.join(simulation_path,"data.lammps")
    params = WriteDataLmp(params,file)
    # =======================================================
    # Write the run file
    file   = os.path.join(simulation_path,"in.lammps")
    params = WriteRunLmp(params,file)
    # =======================================================
    # Execute the run file (name in.lammps and output out.lammps)

    callback() if callback else None
    if callback is not None:
        print_header("Lammps Execution")
        print_header("====================================")


    p_cpu = {"OMP_NUM_THREADS":params["OMP_NUM_THREADS"],
             "mpi":params["mpi"],
             "mpi_np":params["mpi_np"]}
    
    if not params["recompute_dist"]:
        error,cmd =run_lmp(simulation_path,**p_cpu)
        params = ParseLmp(params,file="data.csv")

    else:
        maxiter = 10
        for i in range(maxiter):
            error,cmd =run_lmp(simulation_path,**p_cpu)
            params = ParseLmp(params,file="data.csv")

            r = conse_dist(simulation_path,params["nhilos"])
            params["percent_dist"] = r["percent"]
            if r["percent"] < 20:
                break
            else:
                print("Percent: ",r["percent"],"%")
                print("Recomputing distance")
                
                params["recompute_factor"] = 1+1.25*(i/(maxiter-1))
                params = WriteRunLmp(params,file)
    
    callback() if callback else None

    # =======================================================
    params["cmd"] = cmd
    # save params as json
    # =======================================================
    params["dump_last"] = os.path.join(simulation_path,"data_last.lammps")
    # =======================================================
    return params