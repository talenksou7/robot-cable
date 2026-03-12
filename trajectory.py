import numpy as np

# Robot workspace limits
X_LIMIT = 0.25
Y_LIMIT = 0.235
Z_MIN = 0.1
Z_MAX = 0.45


def inside_workspace(P):
    """
    Check if the platform position P = [x,y,z] is inside the robot workspace
    """
    x, y, z = P
    if -X_LIMIT <= x <= X_LIMIT and -Y_LIMIT <= y <= Y_LIMIT and Z_MIN <= z <= Z_MAX:
        return True
    return False


def trajectory(t):
    """
    Rehabilitation trajectory: forward reach + small vertical assistance
    """

    # motion amplitudes (safe inside workspace)
    Ax = 0.10   # forward/back (10 cm)
    Ay = 0.06   # lateral motion (6 cm)
    Az = 0.05   # vertical assist (5 cm)

    # center height
    z0 = 0.25

    # trajectory equations
    x = Ax * np.sin(t)
    y = Ay * np.sin(t) * np.cos(t)   # figure-8 style lateral motion
    z = z0 + Az * np.sin(t)

    P = np.array([x, y, z])

    # Safety check
    if not inside_workspace(P):
        P = np.clip(P, [-X_LIMIT, -Y_LIMIT, Z_MIN],
                       [X_LIMIT,  Y_LIMIT,  Z_MAX])

    return P