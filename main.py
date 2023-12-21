import cv2 as cv
import numpy as np

url = "images/mcgill.jpeg"
img = cv.imread(url)

if img is None:
    print("Image not found")
    exit()


def process_image(image):
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    image = cv.Canny(image, 100, 150)
    image = cv.rotate(image, cv.ROTATE_180)
    image = cv.flip(image, 1)

    return image


def display_image(image):
    cv.imshow("Awesome Face", image)
    cv.waitKey(0)


def calculate_circle(coord_set):
    a1, a2, a3 = coord_set[0][0], coord_set[1][0], coord_set[2][0]
    b1, b2, b3 = coord_set[0][1], coord_set[1][1], coord_set[2][1]

    a = np.asarray(
        [[-2 * a1 + 2 * a2, -2 * b1 + 2 * b2],
         [-2 * a2 + 2 * a3, -2 * b2 + 2 * b3]])
    b = np.asarray([-(a1 ** 2) - (b1 ** 2) + (a2 ** 2) + (b2 ** 2),
                    -(a2 ** 2) - (b2 ** 2) + (a3 ** 2) + (b3 ** 2)])

    try:
        h, k = np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        print("Inconsistent System", coord_set[0], coord_set[1], coord_set[2])
        return None

    r2 = (a1 - h) ** 2 + (b1 - k) ** 2

    return [h, k, r2]


def is_collinear(coord_set):
    a1, a2, a3 = coord_set[0][0], coord_set[1][0], coord_set[2][0]
    b1, b2, b3 = coord_set[0][1], coord_set[1][1], coord_set[2][1]

    if a1 == a3:
        if a1 == a2:
            return True
        return False

    m = (b3 - b1) / (a3 - a1)

    if (b2 - b1) == m * (a2 - a1):
        return True
    return False


def is_vertical(coord_set):
    a1, a2, a3 = coord_set[0][0], coord_set[1][0], coord_set[2][0]

    if a1 == a2 and a2 == a3:
        return True
    return False


def contains_duplicate(coord_set):
    if np.array_equal(coord_set[0], coord_set[1]) or np.array_equal(coord_set[0], coord_set[2]) \
            or np.array_equal(coord_set[1], coord_set[2]):
        return True
    return False


def calculate_slope(coord_set):
    a1, a3 = coord_set[0][0], coord_set[2][0]
    b1, b3 = coord_set[0][1], coord_set[2][1]

    return (b3 - b1) / (a3 - a1)


def calculate_x_bounds(coord_set):
    minimum = min(coord_set[0][0], coord_set[1][0], coord_set[2][0])
    maximum = max(coord_set[0][0], coord_set[1][0], coord_set[2][0])

    if coord_set[0][0] == minimum:
        min_coord = coord_set[0]
    elif coord_set[0][1] == minimum:
        min_coord = coord_set[1]
    else:
        min_coord = coord_set[2]

    return [minimum, maximum, min_coord]


def calculate_y_bounds(coord_set):
    minimum = min(coord_set[0][1], coord_set[1][1], coord_set[2][1])
    maximum = max(coord_set[0][1], coord_set[1][1], coord_set[2][1])

    if coord_set[0][0] == maximum:
        max_coord = coord_set[0]
    elif coord_set[0][1] == maximum:
        max_coord = coord_set[1]
    else:
        max_coord = coord_set[2]

    return [minimum, maximum, max_coord]


def determine_concavity_vertical(left, circ):
    x, y = left[0], left[1]
    h, k = circ[0], circ[1]

    if y == k:
        # print("0???")
        return 0
    if -1/(y - k) + ((x - h) ** 2) / ((y - k) ** 3) > 0:
        # print("concave up")
        return 1
    elif -1/(y - k) + ((x - h) ** 2) / ((y - k) ** 3) < 0:
        # print("concave down")
        return -1
    else:
        print("huh?", left, circ)


def determine_concavity_horizontal(upper, circ):
    x, y = upper[0], upper[1]
    h, k = circ[0], circ[1]

    if x == h:
        # print("0")
        return 0
    if -1/(x - h) - ((y - k) ** 2) / ((x - h) ** 3) > 0:
        # print("concave right")
        return 1
    elif -1/(x - h) - ((y - k) ** 2) / ((x - h) ** 3) < 0:
        # print("concave left")
        return -1
    else:
        print("huh??", upper, circ)


# determine_concavity_horizontal([2, 276], [51.5, 279.5, 2462.5])


def remove_similar_contours(con):
    contour1 = contours[0]
    contour2 = contours[1]

    # Calculate Hu Moments
    moments1 = cv.moments(contour1)

    moments2 = cv.moments(contour2)

    # Calculate shape similarity using matchShapes
    shape_similarity = cv.matchShapes(contour1, contour2, cv.CONTOURS_MATCH_I1, 0.0)


def get_contour_points(con, frequency):
    count = 0
    coords = []

    print(len(con), "len contours")

    for i in range(len(contours)):
        for j in range(len(con[i])):
            if count == frequency:
                print("(%d, %d)" % (contours[i][j][0][0], contours[i][j][0][1]))
                coords.append([con[i][j][0][0], con[i][j][0][1]])
                count = 0
            else:
                count += 1
        if frequency < len(con[i]):
            coords.append([con[i][frequency][0][0], con[i][frequency][0][1]])
            # print("(%d, %d)" % (contours[i][frequency][0][0], contours[i][frequency][0][1]))

        coords.append([None, None])
    print("len coords:", len(coords))

    threes = []
    i = 0
    while i < len(coords) - 2:
        if coords[i][0] is None or coords[i + 1][0] is None or coords[i + 2][0] is None:
            i += 1
        else:
            threes.append([coords[i], coords[i + 1], coords[i + 2]])
            i += 2
    print("len threes:", len(threes))
    print(threes)
    return np.asarray(threes)


def scale_points(coord_set, scale_factor):
    scaled_points = []
    for i in range(len(coord_set)):
        scaled_points.append(scale_factor * coord_set[i])

    return np.asarray(scaled_points)


def shift_points(coord_set, shift_x, shift_y):
    shifted_points = []
    for i in range(len(coord_set)):
        shifted_points.append([[coord_set[i][0][0] + shift_x, coord_set[i][0][1] + shift_y],
                               [coord_set[i][1][0] + shift_x, coord_set[i][1][1] + shift_y],
                               [coord_set[i][2][0] + shift_x, coord_set[i][2][1] + shift_y]])

    return np.asarray(shifted_points)


img = process_image(img)
contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

display_image(img)

points = get_contour_points(contours, 6)
# points = shift_points(points, 1.9, 4)
# points = scale_points(points, 1)
num_equations = 0

for p in points:
    x_bounds = calculate_x_bounds(p)
    y_bounds = calculate_y_bounds(p)
    if not contains_duplicate(p):
        num_equations += 1
        if is_collinear(p):
            if is_vertical(p):
                print("x = %0.2f \\left\\{%0.2f < y < %0.2f\\right\\}"
                      % (p[0][0], y_bounds[0], y_bounds[1]))
            else:
                slope = calculate_slope(p)
                print("y - %0.2f = %0.2f(x - %0.2f) \\left\\{%0.2f < x < %0.2f\\right\\}"
                      % (p[0][1], slope, p[0][0], x_bounds[0], x_bounds[1]))
        else:
            circle = calculate_circle(p)
            if circle is not None:
                vertical_concavity = determine_concavity_vertical([x_bounds[2][0], x_bounds[2][1]], circle)
                horizontal_concavity = determine_concavity_horizontal([y_bounds[2][0], y_bounds[2][1]], circle)
                if vertical_concavity == 1:
                    if horizontal_concavity == 1:
                        print("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f - 0.7 < x < %0.2f\\right\\} \\left\\{%0.2f - 0.7 < y "
                              "< %0.2f\\right\\}"
                              % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                    else:
                        print("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f < x < %0.2f + 0.7\\right\\} \\left\\{%0.2f - 0.7 < y "
                              "< %0.2f\\right\\}"
                              % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                elif vertical_concavity == -1:
                    if horizontal_concavity == 1:
                        print("(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f - 0.7 < x < %0.2f\\right\\} \\left\\{%0.2f < y "
                              "< %0.2f + 0.7\\right\\}"
                              % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                    else:
                        print(
                            "(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f < x < %0.2f + 0.7\\right\\} \\left\\{%0.2f < y "
                            "< %0.2f + 0.7\\right\\}"
                            % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))
                # else:
                #     print(
                #         "(x - %0.2f)^2 + (y - %0.2f)^2 = %0.2f \\left\\{%0.2f < x < %0.2f\\right\\} \\left\\{%0.2f < y "
                #         "< %0.2f\\right\\}"
                #         % (circle[0], circle[1], circle[2], x_bounds[0], x_bounds[1], y_bounds[0], y_bounds[1]))

print("Number of equations:", num_equations)

