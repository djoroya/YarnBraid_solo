import numpy as np
from model.post.is_fcn.rot_vecs import rot_vecs

def mesh(vector_direccion,translation,size=2):
    # Crear mesh grid en el plano xy
    x = np.linspace(-1.2*size, 1.2*size, 10)
    y = np.linspace(-1.2*size, 1.2*size, 10)
    X, Y = np.meshgrid(x, y)
    Z = 0*X   #
    #
    R = np.sqrt(X**2 + Y**2)
    nan_ms = 0*R + 1
    nan_ms[R>size] = np.nan
    #
    # Transformar el mesh grid al nuevo plano perpendicular al vector dado
    vec = np.array([0, 0, 1])

    if np.sum(np.cross(vec,vector_direccion)) == 0:
        # unit matrix
        rot = np.eye(3)
    else:
        rot = rot_vecs(vec, vector_direccion)

    vec_rot = np.dot(rot, np.vstack([ X.flatten(), 
                                    Y.flatten(), 
                                    Z.flatten()]))

    # Reshape para mantener las dimensiones
    X_trans = np.reshape(vec_rot[0, :] + translation[0], X.shape) 
    Y_trans = np.reshape(vec_rot[1, :] + translation[1], Y.shape) 
    Z_trans = np.reshape(vec_rot[2, :] + translation[2], Z.shape) 
     
    return X_trans, Y_trans, Z_trans, nan_ms