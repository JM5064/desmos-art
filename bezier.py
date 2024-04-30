import numpy as np

def get_functions():
        functions = ["p_{12}(t, p_a, p_b) = (1-t)p_a+tp_b", 
                    "p_{23}(t, p_b, p_c) = (1-t)p_b+tp_c",
                    "p_{34}(t, p_c, p_d) = (1-t)p_c+tp_d",
                    "p_{123}(t, p_a, p_b, p_c) = (1-t)p_{12}(t, p_a, p_b) + tp_{23}(t, p_b, p_c)",
                    "p_{234}(t, p_b, p_c, p_d) = (1-t)p_{23}(t, p_b, p_c) + tp_{34}(t, p_c, p_d)",
                    "p_{1234}(t, p_a, p_b, p_c, p_d) = (1-t)p_{123}(t, p_a, p_b, p_c) + tp_{234}(t, p_b, p_c, p_d)"]

        return functions


def print_functions():
    functions = get_functions()
    for func in functions:
            print(func)


class bezier():

    def __init__(self, points, smoothness=0.4):
        self.points = points
        self.smoothness = smoothness
        self.left_control_points = self.get_left_control_points()
        self.right_control_points = self.get_right_control_points()
    

    def calculate_left_control_point(self, p1, p2, p3):
        l13 = np.subtract(p3, p1)

        if np.linalg.norm(l13) == 0:
             unit_vector = 0
        else:
            unit_vector = l13 / np.linalg.norm(l13)

        l12 = np.subtract(p2, p1)
        length_l12 = np.linalg.norm(l12)

        scaled_vector = -self.smoothness * length_l12 * unit_vector

        return np.add(p2, scaled_vector)



    def calculate_right_control_point(self, p1, p2, p3):
        l13 = np.subtract(p3, p1)

        if np.linalg.norm(l13) == 0:
             unit_vector = 0
        else:
            unit_vector = l13 / np.linalg.norm(l13)

        l23 = np.subtract(p3, p2)
        length_l23 = np.linalg.norm(l23)

        scaled_vector = self.smoothness * length_l23 * unit_vector

        return np.add(p2, scaled_vector)


    def get_left_control_points(self):
        left_control_points = []

        for i in range(len(self.points) - 2):
            p1 = self.points[i]
            p2 = self.points[i+1]
            p3 = self.points[i+2]
            left_control_points.append(self.calculate_left_control_point(p1, p2, p3))

        return left_control_points
    

    def get_right_control_points(self):
        right_control_points = []

        for i in range(len(self.points) - 2):
            p1 = self.points[i]
            p2 = self.points[i+1]
            p3 = self.points[i+2]
            right_control_points.append(self.calculate_right_control_point(p1, p2, p3))
            
        return right_control_points


    def get_curve_equations(self):
        equations = []
        num_points = len(self.points)

        equ = "p_{1234}(t, (%f , %f), (%f , %f), (%f , %f), (%f , %f))"

        equations.append(equ % (self.points[0][0], self.points[0][1], 
                                self.left_control_points[0][0], self.left_control_points[0][1],
                                self.left_control_points[0][0], self.left_control_points[0][1],
                                self.points[1][0], self.points[1][1]))

        for i in range(num_points - 3):
                    equations.append(equ % (self.points[i+1][0], self.points[i+1][1],
                                            self.right_control_points[i][0], self.right_control_points[i][1],
                                            self.left_control_points[i+1][0], self.left_control_points[i+1][1],
                                            self.points[i+2][0], self.points[i+2][1]))


        equations.append(equ % (self.points[num_points-2][0], self.points[num_points-2][1], 
                                self.right_control_points[num_points-3][0], self.right_control_points[num_points-3][1],
                                self.right_control_points[num_points-3][0], self.right_control_points[num_points-3][1],
                                self.points[num_points-1][0], self.points[num_points-1][1]))
                        
        return equations



# a1 = np.array([1,0.5])
# a2 = np.array([1.5,1.2])
# a3 = np.array([2,1.5])
# a4 = np.array([3,2])
# a5 = np.array([4,1.2])
# a6 = np.array([7,2])
# a7 = np.array([4,3])
# a8 = np.array([6,1])
# a9 = np.array([8,1])


# bez = bezier([a1, a2, a3, a4, a5, a6, a7, a8, a9], 0.35)
# print_functions()
# print(bez.left_control_points)
# print(bez.right_control_points)
# print(bez.get_curve_equations())
