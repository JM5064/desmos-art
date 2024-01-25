import cv2 as cv
import utils
import app
import sys
import io

# path = 'images/mcgill.jpeg'
# img = cv.imread(path)
# img = cv.rotate(img, cv.ROTATE_180)
# img = cv.flip(img, 1)

# if img is None:
#     print("Image not found", path)
#     exit()


def get_image(path):
    img = cv.imread(path)

    if img is None:
        print("Image not found")
        exit()

    img = cv.rotate(img, cv.ROTATE_180)
    img = cv.flip(img, 1)

    
    return img


def process_image(image):
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    image = cv.Canny(image, 50, 80)
    # image = cv.rotate(image, cv.ROTATE_180)
    # image = cv.flip(image, 1)

    return image


def display_image(image):
    cv.imshow("Awesome Face", image)
    cv.waitKey(0)


def calculate_points(img):
    processed_img = process_image(img)

    contours, hierarchy = cv.findContours(processed_img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # contours = remove_similar_contours(contours)

    # display_image(processed_img)

    points = utils.get_contour_points(contours, 6)

    # points = shift_points(points, 1.9, 4)
    # points = scale_points(points, 1)

    return points


def get_equations(points, img):
    original_stdout = sys.stdout

    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    num_equations = 0

    for p in points:
        x_bounds = utils.calculate_x_bounds(p)
        y_bounds = utils.calculate_y_bounds(p)
        clr = utils.get_color(p, img)
        print(clr)
        # print("<br>")
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


