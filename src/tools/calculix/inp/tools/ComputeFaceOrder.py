import numpy as np

def vecnormal(matrix):
    # matrix es una matriz de 3x3
    v1 = matrix[1, :] - matrix[0, :]
    v2 = matrix[2, :] - matrix[0, :]
    v =  -np.cross(v1, v2)
    return v / np.linalg.norm(v)


def compute_faces_all(tetra):
    return np.array([tetra[[0, 1, 2, 4, 5, 6]],
                     tetra[[0, 3, 1, 7, 8, 4]],
                     tetra[[1, 3, 2, 9, 5, 8]],
                     tetra[[2, 3, 0, 7, 6, 9]]])


def compute_faces(tetra):
    return np.array([tetra[[0, 1, 2]],
                     tetra[[0, 3, 1]],
                     tetra[[1, 3, 2]],
                     tetra[[2, 3, 0]]])

list_id = np.arange(1, 5)

def ComputeFaceOrder(element_face, nset,select_element):
    # input:
    # - element_face: lista de 4 caras (triangulos)
    # - nset: nodos que forman la superficie
    # - select_element: elemento que se quiere ordenar

    id = set(nset.id_nodes)
    # element_face es una lista de 4 caras (triangulos)
    # element_face es una matriz de 4x3
    # 
    r = [set(iel).issubset(id) for iel in element_face]

    r = list_id[r]

    if len(r) == 0:
        return None
    else:

        element_face = compute_faces_all(select_element)
        r = [set(iel).issubset(id) for iel in element_face]
        r = list_id[r]

        return r
