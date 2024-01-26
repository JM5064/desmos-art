import cv2 as cv
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
        self.image = cv.cvtColor(self.image, cv.COLOR_RGB2GRAY)
        self.image = cv.Canny(self.image, 50, 80)


    def display_image(self):
        cv.imshow("Image", self.image)
        cv.waitKey(0)


    def calculate_points(self):
        self.process_image()
        contours, hierarchy = cv.findContours(self.image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        # contours = remove_similar_contours(contours)

        # display_image(processed_img)

        points = utils.get_contour_points(contours, 6)

        points = utils.shift_points(points, self.shift_x, self.shift_y)
        points = utils.scale_points(points, self.scale_factor)

        return points
    

    def get_color(self, coord_set, image):
        color = image[coord_set[1][1], coord_set[1][0]]

        return utils.bgr_to_hex(color[0], color[1], color[2])


    def get_equations(self, image):
        points = self.calculate_points()

        original_stdout = sys.stdout

        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        num_equations = 0

        for p in points:
            x_bounds = utils.calculate_x_bounds(p)
            y_bounds = utils.calculate_y_bounds(p)
            clr = self.get_color(p, image)
            print(clr)
            if not utils.contains_duplicate(p):
                num_equations += 1
                if utils.is_collinear(p):
                    if utils.is_vertical(p):
                        print("x = %0.2f \\left\\{%0.2f < y < %0.2f\\right\\}"
                            % (p[0][0], y_bounds[0], y_bounds[1]))
                    else:
                        slope = utils.calculate_slope(p)
                        print("y - %0.2f = %0.2f(x - %0.2f) \\left\\{%0.2f < x < %0.2f\\right\\}"
                            % (p[0][1], slope, p[0][0], x_bounds[0], x_bounds[1]))
                else:
                    circle = utils.calculate_circle(p)
                    if circle is not None:
                        vertical_concavity = utils.determine_concavity_vertical([x_bounds[2][0], x_bounds[2][1]], circle)
                        horizontal_concavity = utils.determine_concavity_horizontal([y_bounds[2][0], y_bounds[2][1]], circle)
                        if vertical_concavity == 1:
                            if horizontal_concavity == 1:
                                print("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f "
                                    "\\left\\{%0.2f - 0.7 < x < %0.2f\\right\\} \\left\\{%0.2f - 0.7 < y "
                                    "< %0.2f\\right\\}"
                                    % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                            else:
                                print("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f "
                                    "\\left\\{%0.2f < x < %0.2f + 0.7\\right\\} \\left\\{%0.2f - 0.7 < y < %0.2f\\right\\}"
                                    % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                        elif vertical_concavity == -1:
                            if horizontal_concavity == 1:
                                print("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f "
                                    "\\left\\{%0.2f - 0.7 < x < %0.2f\\right\\} \\left\\{%0.2f < y < %0.2f + 0.7\\right\\}"
                                    % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                            else:
                                print("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f "
                                    "\\left\\{%0.2f < x < %0.2f + 0.7\\right\\} \\left\\{%0.2f < y < %0.2f + 0.7\\right\\}"
                                    % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                                
        print("Number of equations:", num_equations)
        # print("coord_list length:", len(points))

        captured_output = new_stdout.getvalue()
        sys.stdout = original_stdout

        return captured_output


