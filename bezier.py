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

    x_control_points = np.matmul(np.transpose(parameter_matrix), parameter_matrix)
    x_control_points = np.linalg.inv(x_control_points)
    x_control_points = np.matmul(np.linalg.inv(m), x_control_points)
    x_control_points = np.matmul(x_control_points, np.transpose(parameter_matrix))
    x_control_points = np.matmul(x_control_points, x_points)

    y_control_points = np.matmul(np.transpose(parameter_matrix), parameter_matrix)
    y_control_points = np.linalg.inv(y_control_points)
    y_control_points = np.matmul(np.linalg.inv(m), y_control_points)
    y_control_points = np.matmul(y_control_points, np.transpose(parameter_matrix))
    y_control_points = np.matmul(y_control_points, y_points)

    control_points = np.column_stack((np.array(x_control_points)[0], np.array(y_control_points)[0]))

    return control_points


coords = [[1,2],[9,12],[5,6],[3,5]]
# print(calculate_path_length(coords, 3))
# print(calculate_mapped_t_parameter(coords, 3))
# print(get_parameter_matrix(coords))
print()
control_points = get_control_points(coords)
print("(%f, %f)(1-t)^3 + 3(%f, %f)t(1-t)^2 + 3(%f, %f)t^2(1-t) + (%f, %f)t^3" 
      % (control_points[0][0], control_points[0][1], control_points[1][0], control_points[1][1], 
      control_points[2][0], control_points[2][1], control_points[3][0], control_points[3][1]))
# print(get_control_points(coords))
