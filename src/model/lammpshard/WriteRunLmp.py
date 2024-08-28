import numpy as np

def WriteRunLmp(params,file):

    trajs = params["trajs"]

    params["WriteRunLmp"] = file

    lens = [ len(trajs[i]) for i in range(len(trajs))]
    clens = np.cumsum(lens)

    # =======================================================

    if params["Remesh"]:

        dist = params["r0"]

    else:
        fcn = np.mean
    
        dist= [fcn(np.sum(np.diff(trajs[i],axis=0)**2,axis=1)) 
            for i in range(len(trajs))]
    
        dist = fcn(dist)
        dist = np.sqrt(dist)

    # =======================================================

    lammps_file = open(file, "w")

    lines = """
# Initialization
units		real
boundary	p p p
atom_style	molecular
angle_style	zero

read_data	data.lammps extra/bond/per/atom 1

# Force field
#                   kappa  cutoff
pair_style yukawa   yukawa_kappa yukawa_cutoff
pair_coeff * * yukawa_energy
"""

    for i in range(len(trajs)):
        for j in range(i,len(trajs)):
            if i == j:
                lines += "pair_coeff {} {} 0\n".format(i+1,j+1)
            else:
                lines += "pair_coeff {} {} yukawa_energy\n".format(i+1,j+1)

    lines = lines + """
# Bonds 
bond_style harmonic
bond_coeff 1 V0_bond  r0_bond

# angles zero
angle_style harmonic
angle_coeff 1 1500 180.0
angle_coeff 2 1500 90.0

"""
    yukawa_energy = params["yukawa"]["A"]
    yukawa_kappa  = params["yukawa"]["kappa"]
    yukawa_cutoff = params["yukawa"]["cutoff"]

    lines = lines.replace("yukawa_energy",str(yukawa_energy))
    lines = lines.replace("yukawa_kappa",str(yukawa_kappa))

    dist_hilos = 2*params["r_hebra"]

    if yukawa_cutoff is None:
        yukawa_cutoff = 2*params["r_hebra"]
    lines = lines.replace("yukawa_cutoff",str(yukawa_cutoff))
    
    params["radius_compute_per_run"] = dist_hilos

    if dist_hilos < params["r_hebra"]:
        raise Exception("dist_hilos < r_hebra")


    r0_factor = params["r0_factor"]
    lines = lines.replace("r0_bond",str( r0_factor*dist))

    V0_bond       = params["V0_bond"]
    lines = lines.replace("V0_bond",str(V0_bond))

    lammps_file.write(lines)


    clens = clens.tolist()
    clens.insert(0, 0)


    for i in range(len(trajs)):
        lines = "create_bonds  single/bond 1 {} {}".format(clens[i]+1, clens[i+1]) + "\n"
        lammps_file.write(lines)

    RUN_STEPS_EQ = params["RUN_STEPS_EQ"]
    RUN_STEPS_DEFORM = params["RUN_STEPS_DEFORM"]


    
    init_fixed_atom = params["Npoints"]*params["nhilos"]*16 + 1
    end_fixed_atom  =  params["Npoints"]*(params["nhilos"]*16 + params["hilo_central"])
    group_fixed = "group fixed id {}:{}\n".format(init_fixed_atom,end_fixed_atom)
    lammps_file.write(group_fixed)


    # create groups for each yarn
    hilos_central = params["hilo_central"]
    for i in range(len(trajs)-hilos_central):
        lines = "group yarn{} id {}:{}\n".format(i+1,clens[i]+1, clens[i+1])
        lammps_file.write(lines)
        lines = "neigh_modify exclude molecule/intra yarn{}\n".format(i+1)
        lammps_file.write(lines)
        # delete group
        # This is necessary to avoid the creation of new groups
        # in lammps the maximum number of groups is 32
        lines = "group yarn{} delete\n".format(i+1)
        lammps_file.write(lines)

    lines = """


group clump id  1 201 401 601

fix 1 all nvt temp 0.5 0.5 0.01
fix 2 all deform 1 z erate VAR_ERRATE_Z
fix 3 fixed setforce 0.0 0.0 0.0
dump		1 all custom 1000 dump.xyz id type xu yu zu mol

timestep  0.05

run RUN_STEPS_DEFORM
unfix 1
unfix 2
minimize 1e-7 1e-7 100000 100000
fix 1 all nvt temp 1.0 1.0 0.01

run RUN_STEPS_EQ

# save last configuration
write_data data_last.lammps
"""
    lines = lines.replace("RUN_STEPS_EQ"    ,str(RUN_STEPS_EQ))
    lines = lines.replace("RUN_STEPS_DEFORM",str(RUN_STEPS_DEFORM))
    lines = lines.replace("VAR_ERRATE_Z"    ,str(params["errate"]))
    lammps_file.write(lines)

    lammps_file.close()

    return params