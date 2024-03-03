import numpy as np


def calculate_path_length(coord_set, point_num):
    length = 0

    if point_num > len(coord_set):
        point_num = len(coord_set)

    # loop through 0 to point_num and sum distances between points to length
    for i in range(1, point_num + 1):
        length += np.linalg.norm(np.subtract(coord_set[i], coord_set[i-1]))

    return length


def calculate_mapped_t_parameter(coord_set, point_num):
    if point_num == 0:
        return 0
    
    # map each point to its corresponding t value
    point_distance = np.linalg.norm(np.subtract(coord_set[point_num], coord_set[point_num - 1]))
    path_length = calculate_path_length(coord_set, point_num)

    return point_distance / path_length


def get_parameter_matrix(coord_set):
    mat = np.zeros((len(coord_set), 4))


    for i in range(len(mat)):
        t = calculate_mapped_t_parameter(coord_set, i)
        mat[i] = [t ** 3, t ** 2, t, 1]

    return mat
    

def get_control_points(coord_set):
    # matrix to get cubic Bézier curve
    m = np.matrix([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])
    parameter_matrix = get_parameter_matrix(coord_set)

    x_points = np.array(coord_set)[:, 0]
    y_points = np.array(coord_set)[:, 1]

    x_control_points = np.matmul( np.matmul(np.invert(m), np.linalg.inv(parameter_matrix)), x_points)
    y_control_points = np.matmul( np.matmul(np.invert(m), np.linalg.inv(parameter_matrix)), y_points)

    control_points = np.column_stack((np.array(x_control_points)[0], np.array(y_control_points)[0]))

    return control_points



coords = [[1,2], [2,2], [5,3], [6,4]]
print(calculate_path_length(coords, 2))
print(calculate_mapped_t_parameter(coords, 2))
print(get_parameter_matrix(coords))
print()
print(get_control_points(coords))
