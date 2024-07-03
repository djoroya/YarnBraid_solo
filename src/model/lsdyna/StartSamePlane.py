import numpy as np
import pandas as pd

def proyectar(A, O, mvec):
    mvec = mvec/np.linalg.norm(mvec)
    AO_vec = O - A
    if np.dot(AO_vec, AO_vec) < 1e-10:
        return A
    AO_vec_unit = AO_vec/np.linalg.norm(AO_vec)
    Ap_vec = np.dot(AO_vec, mvec)*mvec
    dist = np.sqrt(np.dot(AO_vec, AO_vec) - np.dot(Ap_vec, Ap_vec))

    A_p_plano = O + dist*(np.cross(np.cross(AO_vec_unit, mvec), mvec))
    return A_p_plano


def StartSamePlane(points,npoints, nhilos):

    npoints = npoints
    types = points['type'].unique()
    points_types = [points[points['type'] == itype] for itype in types]
    points_types = [points_type.iloc[:npoints] for points_type in points_types]

    ntrajs = len(points_types)
    # =======================================================
    # Nuevos 4 puntos iniciales	
    # =======================================================
    first_4_pt = [[points_types[j+i].iloc[0, 1:nhilos].values 
               for i in range(nhilos)] 
               for j  in np.arange(0, len(points_types) ,nhilos)]

    second_4_pt = [[points_types[j+i].iloc[1, 1:nhilos].values 
                    for i in range(nhilos)] 
                for j in np.arange(0, len(points_types), nhilos)]

    first_4_pt = np.array(first_4_pt)
    second_4_pt = np.array(second_4_pt)

    vecs = [ np.mean(first_4_pt[j], axis=0) - np.mean(second_4_pt[j], axis=0) 
            for j in range(len(first_4_pt))]

    first_4_pt = [[proyectar(first_4_pt[j][i], first_4_pt[j][0], vecs[j])
                for i in range(nhilos)]
                for j in range(len(first_4_pt))]

    first_4_pt = np.array(first_4_pt)

    new_first_4 = [first_4_pt[i] + vecs[i] 
                   for i in range(len(first_4_pt))]
    new_first_4 = np.array(new_first_4)
    # =======================================================
    # Nuevos 4 puntos finales
    # =======================================================
    end_4_pt = [[points_types[j+i].iloc[-1,
                                        1:nhilos].values 
                                        for i in range(nhilos)] 
                                        for j in np.arange(0, len(points_types), nhilos)]

    be_end_4_pt = [[points_types[j+i].iloc[-2,
                                            1:nhilos].values 
                                            for i in range(nhilos)] 
                                            for j in np.arange(0, len(points_types), nhilos)]

    end_4_pt    = np.array(end_4_pt)
    be_end_4_pt = np.array(be_end_4_pt)


    vecs = [ np.mean(end_4_pt[j], axis=0) - np.mean(be_end_4_pt[j], axis=0) 
            for j in range(len(end_4_pt))]

    end_4_pt = [ [ proyectar(end_4_pt[j][i], end_4_pt[j][0], vecs[j])
                        for i in range(nhilos)              ]
                        for j in range(len(end_4_pt)) ] 
    end_4_pt = np.array(end_4_pt)

    new_end_4 =   [ end_4_pt[i] + vecs[i] 
                for i in range(len(end_4_pt))]

    new_end_4 = np.array(new_end_4)

    # =======================================================

    for iter, j in enumerate(np.arange(0, len(points_types), nhilos)):
        for i in range(nhilos):
            type = points_types[j+i].iloc[0, 0]

            rfirst = new_first_4[iter, i, :]
            rfirst = np.hstack([type, rfirst])
            # 
            rlast = new_end_4[iter, i, :]
            rlast = np.hstack([type, rlast])

            #add new row in first position
            df_old = points_types[j+i]
            points_types[j+i] = pd.DataFrame(np.vstack([rfirst,
                                                        df_old.values,
                                                        rlast]), 
                                                        columns=df_old.columns)

    points_types = pd.concat(points_types, ignore_index=True)
    return points_types