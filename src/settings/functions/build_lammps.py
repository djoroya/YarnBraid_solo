import os
join = os.path.join
download_folder = join(os.getcwd(), "src", "settings", "downloads")
dependen_folder = join(os.getcwd(), "src", "dependences")

def build_lammps():

    if os.name == "nt":
        print("This script is only for linux, please download LAMMPS manually")
        return

    cmd ="cd src/dependences/lammps-stable && mkdir build && cd build && "

    pkgs = ["PKG_MOLECULE", "PKG_CLASS2", "PKG_KSPACE", 
            "PKG_COMPRESS", "PKG_MANYBODY", "PKG_MC",
            "PKG_QEQ", "PKG_USER-INTEL", "PKG_USER-MISC","PKG_FEP",
                "PKG_USER-OMP",  "PKG_EXTRA-PAIR","PKG_DPD-BASIC"]
    cmd_cmake = "cmake ../cmake/"
    for pkg in pkgs:
        cmd_cmake += f" -D {pkg}=yes"

    cmd = cmd + cmd_cmake + " && make -j4"

    # save log 
    cmd = cmd + " > build.log"
    print(cmd)

    os.system(cmd)