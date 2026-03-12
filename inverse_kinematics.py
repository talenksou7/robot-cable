import numpy as np

# Robot frame dimensions (meters)
Lx = 0.50
Ly = 0.47
Lz = 0.50
hx = Lx / 2
hy = Ly / 2
# Anchor points (top corners of frame)
A1 = np.array([-hx, -hy, Lz])
A2 = np.array([ hx, -hy, Lz])
A3 = np.array([ hx,  hy, Lz])
A4 = np.array([-hx,  hy, Lz])

anchors = [A1, A2, A3, A4]


def cable_lengths(P):
    
    lengths = []

    for A in anchors:
        L = np.linalg.norm(P - A)
        lengths.append(L)

    return np.array(lengths)