
import numpy as np
import itertools
# Función para calcular la distancia euclidiana entre dos conjuntos de puntos en 3D
def calcular_distancia_vectorizada(matriz_m, matriz_n):
    # Expandir dimensiones para permitir la resta vectorizada
    m_expandido = np.expand_dims(matriz_m, axis=1)  # (m, 1, 3)
    n_expandido = np.expand_dims(matriz_n, axis=0)  # (1, n, 3)

    # Calcular la distancia euclidiana entre todos los puntos de las dos matrices
    distancias = np.linalg.norm(m_expandido - n_expandido, axis=2)  # (m, n)

    # Encontrar la distancia mínima
    distancia_minima = np.min(distancias)

    return distancia_minima

def search_contacts(df,th=2.5):
    # df es una lista de dataframes
    def disttraj(i, j):
        traj1 = df[i-1].values[:, 1:]
        traj2 = df[j-1].values[:, 1:]
        distancia_minima = calcular_distancia_vectorizada(traj1, traj2)
        return distancia_minima
    ntrajs = len(df)
    contacts = list(itertools.combinations(range(1, ntrajs+1), 2))
    contacts = [list(icontact) for icontact in contacts]
    dist_trajs = [disttraj(ic[0], ic[1]) for ic in contacts]


    contacts = np.array(contacts)
    contacts = contacts[np.array(dist_trajs) < th]
    dist_trajs = np.array(dist_trajs)[np.array(dist_trajs) < th]

    return contacts