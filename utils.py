import numpy as np
import cv2 as cv


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

    a = x - h
    b = y - k

    if b == 0:
        return 0
    if (-a ** 2 - b ** 2) / b ** 3 > 0:
        return 1
    elif (-a ** 2 - b ** 2) / b ** 3 < 0:
        return -1
    else:
        print("huh?", left, circ)


def determine_concavity_horizontal(upper, circ):
    x, y = upper[0], upper[1]
    h, k = circ[0], circ[1]

    a = x - h
    b = y - k

    if a == 0:
        return 0
    if (-a ** 2 - b ** 2) / a ** 3 > 0:
        return 1
    elif (-a ** 2 - b ** 2) / a ** 3 < 0:
        return -1
    else:
        print("huh??", upper, circ)


def calculate_contour_similarity(contour1, contour2):
    return cv.matchShapes(contour1, contour2, cv.CONTOURS_MATCH_I1, 0.0)


def remove_similar_contours(cons):
    unique_contours = []

    for i in cons:
        unique = True
        for j in unique_contours:
            if calculate_contour_similarity(i, j) < 0.01 and len(i) > 30:
                unique = False
                break
        if unique:
            unique_contours.append(i)

    return unique_contours


# pass in the contours, combine the contours by flattening into a reduced list of points (based on frequency)
# split every three points in the new the list of points
def get_threes(contours, frequency):
    count = 0
    coords = []

    # loop over all contours to purge coords
    for i in range(len(contours)):
        # loop over each point in the contour and decide whether to include it or not
        for j in range(len(contours[i])):
            # append every frequency'th point
            if count % frequency == 0:
                coords.append([contours[i][j][0][0], contours[i][j][0][1]])
            count += 1
        # append the last (frequency'th?) point of each contour for a complete curve ???? what does this do
        if frequency < len(contours[i]):
            coords.append([contours[i][frequency][0][0], contours[i][frequency][0][1]])

        # append None to indicate end of contour
        coords.append([None, None])

    # group purged coords into groups of threes
    threes = []
    i = 0
    while i < len(coords) - 2:
        if coords[i][0] is None or coords[i + 1][0] is None or coords[i + 2][0] is None:
            i += 1
        else:
            threes.append([coords[i], coords[i + 1], coords[i + 2]])
            i += 2

    return np.asarray(threes)


def reduce_bezier_contour_points(contours, frequency):
    count = 0
    coords = []

    # loop over all contours to purge coords
    for i in range(len(contours)):
        # loop over each point in the contour and decide whether to include it or not
        for j in range(len(contours[i])):
            # append every frequency'th point, only if the contour is long enough (needed?)
            if len(contours[i]) - len(contours[i]) // frequency >= 3:
                if count % frequency == 0:
                    coords.append([contours[i][j][0][0], contours[i][j][0][1]])
                count += 1
        if frequency < len(contours[i]):
            coords.append([contours[i][frequency][0][0], contours[i][frequency][0][1]])

        # append None to indicate end of contour
        coords.append([None, None])


    # group each contour back together
    curves = []
    i = 0
    while i < len(coords):
        curve = []
        while coords[i][0] is not None:
            curve.append(coords[i])
            i += 1
        i += 1
        
        if len(curve) > 2:
            curves.append(curve)
    
    return curves
    

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


def bgr_to_hex(b, g, r):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

