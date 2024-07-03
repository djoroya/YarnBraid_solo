import numpy as np

def douglas_peucker_3d(points, epsilon):
    if len(points) <= 2:
        return points

    # Encontrar el punto con la distancia máxima
    dmax = 0
    index = 0
    end = len(points)

    for i in range(1, end - 1):
        d = perpendicular_distance_3d(points[i], (points[0], points[end - 1]))
        if d > dmax:
            index = i
            dmax = d

    # Si la distancia máxima es mayor que epsilon, recursivamente simplificar
    if dmax > epsilon:
        rec_results1 = douglas_peucker_3d(points[:index + 1], epsilon)
        rec_results2 = douglas_peucker_3d(points[index:], epsilon)

        # Concatenar los resultados
        result = np.vstack((rec_results1[:-1], rec_results2))
    else:
        result = np.array([points[0], points[-1]])

    return result

def perpendicular_distance_3d(point, line):
    # Calcular la distancia perpendicular de un punto a una línea en 3D
    x0, y0, z0 = point
    x1, y1, z1 = line[0]
    x2, y2, z2 = line[1]

    numerator = np.linalg.norm(np.cross(np.array([x2 - x1, y2 - y1, z2 - z1]), np.array([x1 - x0, y1 - y0, z1 - z0])))
    denominator = np.linalg.norm(np.array([x2 - x1, y2 - y1, z2 - z1]))

    return numerator / denominator

# # Ejemplo de uso:
# # points es tu array de puntos (x, y, z)
# points_3d = np.array([
#     [0, 0, 0],
#     [1, 1, 1],
#     [2, 2, 2],
#     [3, 3, 3],
#     [4, 4, 4],
#     [5, 5, 5]
# ])

# epsilon_3d = 0.5  # Ajusta este valor según tus necesidades

# simplified_points_3d = douglas_peucker_3d(points_3d, epsilon_3d)
# print(simplified_points_3d)
