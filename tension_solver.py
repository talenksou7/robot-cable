import numpy as np

def compute_tensions(P, anchors, m=10):

    g = 9.81

    U = []

    for A in anchors:

        cable = A - P

        u = cable / np.linalg.norm(cable)

        U.append(u)

    U = np.array(U).T

    W = np.array([0, 0, m*g])

    T = np.linalg.lstsq(U, W, rcond=None)[0]

    return T    