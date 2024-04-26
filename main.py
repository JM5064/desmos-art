import cv2 as cv
import numpy as np
import utils
import sys
import io
import bezier


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
        # self.image = cv.blur(self.image, (2,3))
        self.image = cv.blur(self.image, (3,3))
        # self.image = cv.blur(self.image, (4,4))
        # self.image = cv.blur(self.image, (5,5))
        # self.image = cv.blur(self.image, (6,6))
        self.image = cv.cvtColor(self.image, cv.COLOR_RGB2GRAY)
        self.image = cv.Canny(self.image, 30, 50)


    def display_image(self):
        cv.imshow("Image", self.image)
        cv.waitKey(0)

    
    def get_contours(self):
        self.process_image()

        contours, hierarchy = cv.findContours(self.image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        # contours = utils.remove_similar_contours(contours)

        return contours


    def calculate_circle_points(self, contours):        
        points = utils.get_threes(contours, 10)

        points = utils.shift_points(points, self.shift_x, self.shift_y)
        points = utils.scale_points(points, self.scale_factor)

        return points
    

    def get_color(self, coord_set, image):
        color = np.array(image[coord_set[1][1], coord_set[1][0]], np.int16)

        return utils.bgr_to_hex(color[0], color[1], color[2])
    

    def calculate_bezier_points(self, contours):
        points = utils.reduce_bezier_contour_points(contours, 2)

        # points = utils.shift_points(points, self.shift_x, self.shift_y)
        # points = utils.scale_points(points, self.scale_factor)

        return points
    

    def print_bezier_equations(self):
        contours = self.get_contours

        reduced_contours = self.calculate_bezier_points(contours)

        for contour in reduced_contours:
            # print("contour test: ", contour)
            # print("first point:", contour[0][0])
            curve = bezier.bezier(contour)

            curve.get_curve_equations()
            # break


    def get_circle_line_equations(self, image):
        equations = []

        contours = self.get_contours()
        threes = self.calculate_circle_points(contours)

        for points in threes:
            x_bounds = utils.calculate_x_bounds(points)
            y_bounds = utils.calculate_y_bounds(points)

            clr = self.get_color(points, image)
            equations.append(clr)

            if utils.is_collinear(points):
                # get line if collinear
                line_equation = self.get_line_equation(points, x_bounds, y_bounds)

                if line_equation is not None:
                    equations.append(self.get_line_equation(points, x_bounds, y_bounds))
            else:
                # get circle if not collinear
                circle_equation = self.get_circle_equation(points, x_bounds, y_bounds)
                
                if circle_equation is not None:
                    equations.append(circle_equation)
                                                                
        return equations
    

    def get_line_equation(self, points, x_bounds, y_bounds):
        if not utils.contains_duplicate(points):
            if utils.is_vertical(points):
                return "x = %0.2f \\left\\{%0.2f < y < %0.2f\\right\\}" % (points[0][0], y_bounds[0], y_bounds[1])
            else:
                slope = utils.calculate_slope(points)

                return "y - %0.2f = %0.2f(x - %0.2f) \\left\\{%0.2f < x < %0.2f\\right\\}" % (points[0][1], slope, points[0][0], x_bounds[0], x_bounds[1])
        

    def get_circle_equation(self, points, x_bounds, y_bounds):
        if utils.contains_duplicate(points):
            return None

        circle = utils.calculate_circle(points)

        if circle is None:
            return None
        
        vertical_concavity = utils.determine_concavity_vertical([x_bounds[2][0], x_bounds[2][1]], circle)
        horizontal_concavity = utils.determine_concavity_horizontal([y_bounds[2][0], y_bounds[2][1]], circle)
        
        if vertical_concavity == 1:
            if horizontal_concavity == 1:
                return "(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f - 0.7 < x < %0.2f\\right\\} \\left\\{%0.2f - 0.7 < y < %0.2f\\right\\}" % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1])
            else:
                return "(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f < x < %0.2f + 0.7\\right\\} \\left\\{%0.2f - 0.7 < y < %0.2f\\right\\}" % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1])
        elif vertical_concavity == -1:
            if horizontal_concavity == 1:
                return "(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f - 0.7 < x < %0.2f\\right\\} \\left\\{%0.2f < y < %0.2f + 0.7\\right\\}" % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1])
            else:
                return "(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f < x < %0.2f + 0.7\\right\\} \\left\\{%0.2f < y < %0.2f + 0.7\\right\\}" % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1])
    

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




