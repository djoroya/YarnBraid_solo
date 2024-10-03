import numpy as np
from scipy.linalg import svd
# 
def plane_svd(puntos):
    # Centrar los puntos en el origen
    mean = np.mean(puntos, axis=0)
    puntos_cent = puntos - mean
    
    # Realizar SVD para encontrar los vectores propios
    _, _, vh = svd(puntos_cent, full_matrices=False)
    
    # El vector propio con el valor propio más pequeño es normal al plano
    m = vh[-1,:]
    
    # Calcular D como el producto punto negativo del vector normal 
    # y cualquier punto del plano
    
    # Función para proyectar un punto en el plano
    m_hat = m/np.linalg.norm(m)
    def proyectar_punto(punto):
        t = np.dot(m_hat, mean-punto)
        p_proyected = punto + t * m
        return p_proyected
    
    # Proyectar todos los puntos
    puntos_proyectados = np.array([proyectar_punto(punto) 
                                   for punto in puntos])
    
    # Regresar los puntos proyectados, el vector normal y D

    return puntos_proyectados, m

# 
def plane_alinear(puntos,puntos_ref):
    # Centrar los puntos en el origen
    mean_ref = np.mean(puntos_ref, axis=0)
    puntos_cent = puntos_ref - mean_ref
    
    # Realizar SVD para encontrar los vectores propios
    _, _, vh = svd(puntos_cent, full_matrices=False)
    
    # El vector propio con el valor propio más pequeño es normal al plano
    m = vh[-1,:]
    
    # Calcular D como el producto punto negativo del vector normal 
    # y cualquier punto del plano
    
    # Función para proyectar un punto en el plano
    m_hat = m/np.linalg.norm(m)
    mean = np.mean(puntos, axis=0)
    def proyectar_punto(punto):
        t = np.dot(m_hat, mean-punto)
        p_proyected = punto + t * m
        return p_proyected
    
    # Proyectar todos los puntos
    puntos_proyectados = np.array([proyectar_punto(punto) 
                                   for punto in puntos])
    
    # Regresar los puntos proyectados, el vector normal y D

    return puntos_proyectados