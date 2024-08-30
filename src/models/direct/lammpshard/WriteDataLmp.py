import numpy as np

def WriteDataLmp(params,name_file):

    h               = params['h']
    Npoints         = params['Npoints']
    hilo_central    = params['hilo_central']
    factor          = params['factor']
    trajs           = params['trajs']
    nhilos          = params['nhilos']
    params["WriteDataLmp"] = name_file

    # =======================================================
    # Limits of box
    # =======================================================
    x_lim = [ np.min(trajs[0][:,0]) , np.max(trajs[0][:,0]) ]
    y_lim = [ np.min(trajs[0][:,1]) , np.max(trajs[0][:,1]) ]

    x_lim = [ x_lim[0]*factor, x_lim[1]*factor]
    y_lim = [ y_lim[0]*factor, y_lim[1]*factor]

    z_lim = [0, h]

    # =======================================================
    # Initial parameters
    # =======================================================
    file = open(name_file, "w")

    Ntrajs = len(trajs)
    Natoms = np.sum([trajs[i].shape[0] for i in range(Ntrajs)])
    line = "\n\t" + str(Natoms) + " atoms\n"
    file.write(line)
    Nbonds = np.sum([trajs[i].shape[0]-1 for i in range(Ntrajs)])
    line = "\t"+str(Nbonds) + " bonds\n"
    file.write(line)

    Nangles = (nhilos-2)*Npoints*16
    Nangles = Nangles +  16*(Npoints-1) # ortogonal angles
    # 
    Nangles = Nangles + 64*(Npoints-2) # 123 - 234 - 345 - 456 - 567 - 678 - 781 - 812

    line = "\t"+str(Nangles) + " angles\n\n"
    file.write(line)


    lines = "\t" + str(Ntrajs) + " atom types\n"
    file.write(lines)

    lines = """    1 bond types
        3 angle types
        0 dihedrals types
        0 impropers types

    """
    
    file.write(lines)

    # =======================================================
    # Box
    # =======================================================
    limits = [x_lim, y_lim, z_lim]
    label = ['x', 'y', 'z']
    factor = 1.01
    for i, ilim in enumerate(limits):
        lines = "\t" + str(factor*ilim[0]) + " " + \
            str(factor*ilim[1]) + " " + \
            label[i] + "lo " + label[i] + "hi\n"
        file.write(lines)

    lines = "\t0. 0. 0. xy xz yz\n"
    file.write(lines)


    lines = "Masses\n\n"
    file.write(lines)

    for i in range(Ntrajs):
        lines = "\t" + str(i+1) + " 1.0\n"
        file.write(lines)

    # =======================================================
    # Position of atoms
    # =======================================================


    lines = "\nAtoms\n\n"
    file.write(lines)

    # atom position
    id_atom = 1
    for j in range(len(trajs)):
        traj1_x = trajs[j][:, 0]
        traj1_y = trajs[j][:, 1]
        traj1_z = trajs[j][:, 2]

        N = len(traj1_x)
        for i in range(N):
            x, y, z = traj1_x[i], traj1_y[i], traj1_z[i]
            line = str(id_atom) + " " + str(j+1) + " " + \
                str(j+1)+" " + \
                str(x) + " " + \
                str(y) + " " + \
                str(z) + "\n"
            file.write(line)
            id_atom += 1

    # =======================================================
    # Bonds
    # =======================================================

    lines = "\nBonds\n\n"
    file.write(lines)
    # Yarns bonds
    # Este enlace es entre los puntos de la misma fibra
    id_atom = 0
    id_bound = 1
    for j in range(Ntrajs):
        N = len(trajs[j])
        for i in range(N-1):
            line = str(id_bound) + " 1 " + str(id_atom+1) + \
                " " + str(id_atom+2) + "\n"
            file.write(line)
            id_atom += 1
            id_bound += 1
        id_atom += 1

    # =======================================================
    # Angles
    # =======================================================
    # Estos angulos son entre los puntos de la distintas fibras
    # mantienen 4 fibras formando 180 grados
    # de manera que las cuatro fibras forman un cinta
    # =======================================================
    lines = """
    Angles

    """
    file.write(lines)

    idx_160 = np.arange(0,Npoints,1)
    angle_id = 1
    for id in np.arange(0,Ntrajs-hilo_central,nhilos):
        idx = np.arange(id,id+nhilos)
        for i in range(nhilos-2):
            tri = idx[i:i+(nhilos-1)]
            index_1 = idx_160 + tri[0]*Npoints + 1
            index_2 = idx_160 + tri[1]*Npoints + 1
            index_3 = idx_160 + tri[2]*Npoints + 1

            for k in range(len(index_1)):
                line = str(angle_id) + " 1 " + str(index_1[k]) + \
                    " " + str(index_2[k]) + " " + str(index_3[k]) + "\n"
                file.write(line)
                angle_id += 1

    # =======================================================
    # Angles
    # =======================================================
    # Ortogonal angles
    #add ortogonal angles
    angle_id = angle_id -1

    for i in range(16):
        for k in range(Npoints-1):
            start = (i)*nhilos*Npoints
            angle_id += 1

            line = "{} 2 {} {} {}\n".format(angle_id            , 
                                            start+2+k           , 
                                            start+1+k           , 
                                            start+Npoints+1+k)
            file.write(line)

    # =======================================================
    # Angles 
    # =======================================================
    # 123 - 234 - 345 - 456 - 567 - 678 - 781 - 812 
    # en cada fibra
    # =======================================================

    for i in range(64):
        N = len(trajs[i])
        for j in range(N-2):
            line = "{} 3 {} {} {}\n".format(angle_id            , 
                                            j+1+i*Npoints       , 
                                            j+2+i*Npoints       , 
                                            j+3+i*Npoints)
            file.write(line)
            angle_id += 1

    file.close()

    return params
