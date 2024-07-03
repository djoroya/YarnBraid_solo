import os
from settings.settings import settings

settings = settings()
lmp = settings["lmp"]
# comprobar que lmp existe
if not os.path.isfile(lmp):
    raise Exception("lammps executable not found in {}".format(lmp))

def run_lmp(output_folder,OMP_NUM_THREADS=1,mpi=False,mpi_np=4):
    """
    Run lammps in a given folder.
    """
    os.environ["OMP_NUM_THREADS"] = str(OMP_NUM_THREADS)

    curr = os.getcwd()
    abs_out = os.path.abspath(output_folder)
    os.chdir(output_folder)

    if os.name == "nt":
        if mpi:
            cmd = "mpiexec -n {} ".format(mpi_np)
            cmd += '"'+lmp+'" -in in.lammps > out.lammps'
        else:   
            cmd = '"'+lmp+'" -in in.lammps > out.lammps'
        print(cmd)
        # show output files path
        print("Output file: "+os.path.join(abs_out,"out.lammps"))
        error = os.system(cmd)
        os.chdir(curr)
    else:
        os.environ["OMP_NUM_THREADS"] = "2"
        np = 4
        mpirun = "mpirun -np {} ".format(np)
        cmd = mpirun+lmp+" -in in.lammps > out.lammps"
        error = os.system(cmd)

    os.chdir(curr)
    return error,cmd