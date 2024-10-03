import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

def smooth_trajectory_fourier(trajectory, cutoff=0.1):
    """
    Suaviza una trayectoria tridimensional eliminando frecuencias altas mediante la Transformada de Fourier.
    
    Args:
    - trajectory (np.ndarray): Trayectoria en 3D (Nx3 array).
    - cutoff (float): Fracción de las frecuencias más altas a eliminar (entre 0 y 1).

    Returns:
    - np.ndarray: Trayectoria suavizada.
    """
    # Número de puntos en la trayectoria
    n_points = trajectory.shape[0]

    # 
    trajectory_reverse = np.flip(trajectory, axis=0)
    trajectory = np.concatenate((trajectory, trajectory_reverse), axis=0)
    n_points = trajectory.shape[0]

    # Aplicar FFT a cada una de las componentes x, y, z
    trajectory_fft_x = np.fft.fft(trajectory[:, 0])
    trajectory_fft_y = np.fft.fft(trajectory[:, 1])
    trajectory_fft_z = np.fft.fft(trajectory[:, 2])

    # Crear un filtro de frecuencias
    frequencies = np.fft.fftfreq(n_points)
    
    # Filtro pasa bajas: solo dejamos las frecuencias bajas (filtros de Fourier son simétricos)
    high_freq_idx = np.abs(frequencies) > cutoff
    trajectory_fft_x[high_freq_idx] = 0
    trajectory_fft_y[high_freq_idx] = 0
    trajectory_fft_z[high_freq_idx] = 0

    # Transformada Inversa de Fourier para obtener la trayectoria suavizada
    smooth_x = np.fft.ifft(trajectory_fft_x).real
    smooth_y = np.fft.ifft(trajectory_fft_y).real
    smooth_z = np.fft.ifft(trajectory_fft_z).real

    # Reconstruir la trayectoria suavizada
    smoothed_trajectory = np.vstack((smooth_x, smooth_y, smooth_z)).T

    # tomar solo la mitad de la trayectoria
    smoothed_trajectory = smoothed_trajectory[:n_points//2]

    return smoothed_trajectory