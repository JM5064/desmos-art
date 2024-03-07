import numpy as np


def calculate_bisector_control_point(p1, p2, p3):
    # check for collinear

    hyp = np.subtract(np.array(p3), np.array(p1))   # c
    p12 = np.subtract(np.array(p2), np.array(p1))   # a
    midpoint = np.add(p1, p2) * 0.5

    A = np.asarray([ [hyp[1], -hyp[0]],  [p12[0], p12[1]] ])
    b = np.asarray([ [p2[0] * hyp[1] - p2[1] * hyp[0]],   [p12[0] * midpoint[0] + p12[1] * midpoint[1]] ])
    
    try:
        x, y = np.linalg.solve(A, b)
        return [x, y]
    
    except np.linalg.LinAlgError:
        print("Inconsistent system", A, b)
        return None

# print(calculate_bisector_control_point([1,0.5], [2,1], [4,1]))
print(calculate_bisector_control_point([6,0], [4,1], [2,1]))
print(calculate_bisector_control_point([18,13], [8,11], [4,6]))


