import os
import time
from tools.viewer.viewer import luncher
import pandas as pd
from settings.settings import settings
import subprocess
import signal

settings = settings()
calculix         = settings["calculix"]
calculix_dynamic = settings["calculix_dynamic"]

def runccx(output_folder,
           name_inp,
           att              = 4,
           OMP_NUM_THREADS  = 8,
           outtxt           = "out.txt",
           dynamic          = False,
           mpi              = False,
           mpi_np           = 4):

    if dynamic:
        ccx = calculix_dynamic
    else:
        ccx = calculix

    # ==============================================================================
    # viewer function
    # ==============================================================================
    def viewer(elapsed,p):
        nlines_showed = p["nlines_showed"]
        outfile = os.path.join(name_inp+".cvg")
        exist = os.path.isfile(outfile)
        if exist:
            lines = open(outfile).readlines()
            nlines = len(lines)
        else:
            lines = ".cvg file not found"
            nlines = 0
        # use div html to show lines
        # mono space
        sec = elapsed%60
        minu = elapsed//60
        hour = minu//60
        if nlines_showed < nlines:
            print(lines[p["nlines_showed"]].replace("\n",""))
            p["nlines_showed"] = p["nlines_showed"] + 1
        
        if nlines_showed == 0:
            time.sleep(10)

    # ==============================================================================
    # stopper function
    # ==============================================================================
    
    def stopper():
        cvf_file = name_inp+".cvg"
        try:
            # count lines
            nlines = sum(1 for line in open(cvf_file))
            if nlines < 5:
                return False
            # read last line
            df_cvf = pd.read_csv(cvf_file, sep=r"\s+", header=None,skiprows=4)
            last_row = df_cvf.iloc[-1,:]
            # 0 STEP , 1 INC
            # 2 ATT  , 3 ITER
            # 4 CONT EL (#)
            att = last_row[2]
            # condicion de parada
            if att > att:
                # read pid.txt and kill process
                pid = int(open("pid.txt").read())
                print("Killing process: ",pid)
                os.kill(pid,signal.SIGTERM)
                return True
            else:
                return False
        except:
            print("Error reading cvf file")
            return False
        
    # ==============================================================================
    curr_dir = os.getcwd()
    out_abs = os.path.abspath(output_folder)
    os.chdir(output_folder)

    os.environ["OMP_NUM_THREADS"] = str(OMP_NUM_THREADS)  # Establece el número deseado de hilos

    # ==============================================================================
    # if windows
    if os.name == "nt":
        if mpi:
            # evitamos los problemas con los espacios en blanco
            ccx_path_without_sep = ccx.replace(" ","_SEP_")
            cmd = ccx_path_without_sep+' {}'.format(name_inp)
            cmd = 'mpiexec -n {} '.format(mpi_np) + cmd
        else:
            cmd = ccx+' {}'.format(name_inp)

    else:   
        # if linux
        cmd = "{} {} > ".format(ccx,name_inp) +outtxt
    # ==============================================================================
    # De esta menra evitamos los probelemas con los espacios en blanco
    # en las direcciones de los archivos
    # ==============================================================================
    cmd_split = cmd.split(" ")
    if mpi:
        cmd_split = [ line.replace("_SEP_"," ") for line in cmd_split
                     ]
    print("Running Calculix at: ",output_folder)
    # show the outpt file 
    print("Output file: ", os.path.join(out_abs,outtxt))
    print("Command:\n",cmd)
    @luncher(viewer,stopper)
    def run():
        stdout = open(outtxt,"w")
        stderr = open("err.txt","w")
        process = subprocess.Popen(cmd_split,
                                    stdout = stdout,
                                    stderr = stderr)
        # save pid in pid.txt
        pid = process.pid
        print("\npid: ",pid,"\n")
        with open("pid.txt","w") as f:
            f.write(str(pid))
        # wait for process to finish
        process.wait()
        
    try:
        run()
        error = 0
    except Exception as e:
        error = 1
        os.chdir(curr_dir)
        raise Exception(e)

    print("Calculix finished\n")
    os.chdir(curr_dir)

    return error,cmd


