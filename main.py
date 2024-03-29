import cv2 as cv
import numpy as np
import utils
import sys
import io


def get_image(path):
        img = cv.imread(path)

        if img is None:
            print("Image not found")
            return None

        img = cv.rotate(img, cv.ROTATE_180)
        img = cv.flip(img, 1)

        
        return img


class EquationImage:

    def __init__(self, image, color=True, shift_x=0, shift_y=0, scale_factor=1):
        self.image = image
        self.color = color
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.scale_factor = scale_factor


    def process_image(self):
        self.image = cv.blur(self.image, (3,3))
        self.image = cv.cvtColor(self.image, cv.COLOR_RGB2GRAY)
        self.image = cv.Canny(self.image, 20, 30)


    def display_image(self):
        cv.imshow("Image", self.image)
        cv.waitKey(0)


    def calculate_points(self):
        self.process_image()
        contours, hierarchy = cv.findContours(self.image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        # contours = utils.remove_similar_contours(contours)

        # self.display_image()

        points = utils.get_threes(contours, 10)

        points = utils.shift_points(points, self.shift_x, self.shift_y)
        points = utils.scale_points(points, self.scale_factor)

        return points
    

    def get_color(self, coord_set, image):
        color = np.array(image[coord_set[1][1], coord_set[1][0]], np.int16)

        # if abs(color[0] - color[1]) < 30 and abs(color[0] - color[2]) < 30:
        #     color[0] += 40
        #     if color[0] > 255:
        #         color[0] = 255
        #     color[1] += 40
        #     if color[1] > 255:
        #         color[1] = 255
        #     color[2] += 40
        #     if color[2] > 255:
        #         color[2] = 255

        return utils.bgr_to_hex(color[0], color[1], color[2])


    def get_circle_equations(self, image):
        equations = []

        threes = self.calculate_points()

        for points in threes:
            x_bounds = utils.calculate_x_bounds(points)
            y_bounds = utils.calculate_y_bounds(points)
            clr = self.get_color(points, image)
            equations.append(clr)
            if not utils.contains_duplicate(points):
                if utils.is_collinear(points):
                    if utils.is_vertical(points):
                        equations.append("x = %0.2f \\left\\{%0.2f < y < %0.2f\\right\\}"
                            % (points[0][0], y_bounds[0], y_bounds[1]))
                    else:
                        slope = utils.calculate_slope(points)
                        equations.append("y - %0.2f = %0.2f(x - %0.2f) \\left\\{%0.2f < x < %0.2f\\right\\}"
                            % (points[0][1], slope, points[0][0], x_bounds[0], x_bounds[1]))
                else:
                    circle = utils.calculate_circle(points)
                    if circle is not None:
                        vertical_concavity = utils.determine_concavity_vertical([x_bounds[2][0], x_bounds[2][1]], circle)
                        horizontal_concavity = utils.determine_concavity_horizontal([y_bounds[2][0], y_bounds[2][1]], circle)
                        if vertical_concavity == 1:
                            if horizontal_concavity == 1:
                                equations.append("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f "
                                    "\\left\\{%0.2f - 0.7 < x < %0.2f\\right\\} \\left\\{%0.2f - 0.7 < y "
                                    "< %0.2f\\right\\}"
                                    % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                            else:
                                equations.append("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f "
                                    "\\left\\{%0.2f < x < %0.2f + 0.7\\right\\} \\left\\{%0.2f - 0.7 < y < %0.2f\\right\\}"
                                    % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                        elif vertical_concavity == -1:
                            if horizontal_concavity == 1:
                                equations.append("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f "
                                    "\\left\\{%0.2f - 0.7 < x < %0.2f\\right\\} \\left\\{%0.2f < y < %0.2f + 0.7\\right\\}"
                                    % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                            else:
                                equations.append("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f "
                                    "\\left\\{%0.2f < x < %0.2f + 0.7\\right\\} \\left\\{%0.2f < y < %0.2f + 0.7\\right\\}"
                                    % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                                                                
        return equations
    

    def get_printed_equations(self, equations):
        original_stdout = sys.stdout

        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        for equation in equations:
            print(equation)

        captured_output = new_stdout.getvalue()
        sys.stdout = original_stdout

        return captured_output
    

    def get_num_equations(self, equations):
        return len(equations)




