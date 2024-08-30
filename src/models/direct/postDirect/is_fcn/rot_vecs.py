import numpy as np

def rot_vecs(v1, v2):
    # Normalizar vectores
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)

    # Calcular el producto cruz entre los vectores
    v_cross = np.cross(v1, v2)

    # Calcular el ángulo de rotación
    cos_theta = np.dot(v1, v2)
    sin_theta = np.linalg.norm(v_cross)

    # Matriz de rotación
    skew_matrix = np.array([[0, -v_cross[2], v_cross[1]],
                            [v_cross[2], 0, -v_cross[0]],
                            [-v_cross[1], v_cross[0], 0]])

    R = np.eye(3) + \
        skew_matrix + \
        np.dot(skew_matrix, skew_matrix) * ((1 - cos_theta) / sin_theta**2)

    return R