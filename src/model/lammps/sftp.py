import sys 
import os 
# colors in terminal
from colorama import Fore

def sftp(name):
    file_full = "/home/djoroya/projects/DIMAT/01_TECNORED_BRAID/01_LAMMPS/output/{}/dump.xyz".format(name)
    cmd = "sftp://djoroya@192.168.1.238/" + file_full + "\n"

    # comprobar que el archivo existe
    if not os.path.exists(file_full):
        print("\n"+Fore.RED+
              "The file {} does not exist\n".format(file_full))
        return 1
    else:
        print("\n "+Fore.GREEN + cmd + Fore.RESET)
        return 0

sftp(sys.argv[1])
