import numpy as np


class bezier():

    def __init__(self, points, smoothness=0.4):
        self.points = points
        self.smoothness = smoothness


    def print_functions():
        print("x_{12}(t, x_a, x_b) = (1-t)x_a+tx_b")
        print("y_{12}(t, y_a, y_b) = (1-t)y_a+ty_b")

        print("x_{23}(t, x_b, x_c) = (1-t)x_b+tx_c")
        print("y_{23}(t, y_b, y_c) = (1-t)y_b+ty_c")

        print("x_{34}(t, x_c, x_d) = (1-t)x_c+tx_d")
        print("y_{34}(t, y_c, y_d) = (1-t)y_c+ty_d")

        print("x_{123}(t, x_a, x_b, x_c) = (1-t)x_{12}(t, x_a, x_b) + tx_{23}(t, x_b, x_c)")
        print("y_{123}(t, y_a, y_b, y_c) = (1-t)y_{12}(t, y_a, y_b) + ty_{23}(t, y_b, y_c)")

        print("x_{234}(t, x_b, x_c, x_d) = (1-t)x_{23}(t, x_b, x_c) + tx_{34}(t, x_c, x_d)")
        print("y_{234}(t, y_b, y_c, y_d) = (1-t)y_{23}(t, y_b, y_c) + ty_{34}(t, y_c, y_d)")

        print("x_{1234}(t, x_a, x_b, x_c, x_d) = (1-t)x_{123}(t, x_a, x_b, x_c) + tx_{234}(t, x_b, x_c, x_d)")
        print("y_{1234}(t, y_a, y_b, y_c, y_d) = (1-t)y_{123}(t, y_a, y_b, y_c) + ty_{234}(t, y_b, y_c, y_d)")


    def calculate_left_control_point(self, p1, p2, p3):
        l13 = np.subtract(p3, p1)
        unit_vector = l13 / np.linalg.norm(l13)

        l12 = np.subtract(p2, p1)
        length_l12 = np.linalg.norm(l12)

        scaled_vector = -self.smoothness * length_l12 * unit_vector

        return np.add(p2, scaled_vector)



    def calculate_right_control_point(self, p1, p2, p3):
        l13 = np.subtract(p3, p1)
        unit_vector = l13 / np.linalg.norm(l13)

        l23 = np.subtract(p3, p2)
        length_l23 = np.linalg.norm(l23)

        scaled_vector = self.smoothness * length_l23 * unit_vector

        return np.add(p2, scaled_vector)

    print_functions()


a1 = np.array([1,0.5])
a2 = np.array([1.5,1.2])
a3 = np.array([2,1.5])

bez = bezier([])
print(bez.calculate_left_control_point(a1, a2, a3))
print(bez.calculate_right_control_point(a1, a2, a3))
