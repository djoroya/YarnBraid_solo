from models.direct.lammpsperiodic.curve        import curve
from models.direct.lammpsperiodic.WriteDataLmp import WriteDataLmp 
from models.direct.lammpsperiodic.WriteRunLmp  import WriteRunLmp
from models.direct.lammpsperiodic.ParseLmp     import ParseLmp
import os
from tools.step.runstep import runstep,address
import numpy as np
from tools.lammps.run_lmp import run_lmp
import colorama



def print_header(header):
    print(colorama.Fore.GREEN + header + colorama.Style.RESET_ALL)


@runstep(address(__file__))
def RunLammps(params,output_folder,callback=None):

    # len_periodic can be [1/8, 1/4, 1/2]
    assert params["len_periodic"] in [1/8, 1/4, 1/2,1], "len_periodic must be in [1/8, 1/4, 1/2]"

    if params["only_small"]:
        params["len_periodic"] = 1/8
        params["Npoints"] = int(params["Npoints"]/8)

    callback(nstep=2) if callback else None

    #
    simulation_path = params["output_folder"]

    N     = params["nhilos"]
    rho   = params["r_hebra"]
    theta = params["theta"]
    th_hebra = params["th_hebra"]
    params["h"] = 16*N*(rho+th_hebra)/np.sin(np.pi/2 - theta)


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
    
    error,cmd =run_lmp(simulation_path,**p_cpu)
    params = ParseLmp(params,file="data.csv")


    
    callback() if callback else None

    # =======================================================
    params["cmd"] = cmd
    # save params as json
    # =======================================================
    params["dump_last"] = os.path.join(simulation_path,"data_last.lammps")
    # =======================================================
    return params