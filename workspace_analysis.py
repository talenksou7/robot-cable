import numpy as np
import matplotlib.pyplot as plt
from tension_solver import compute_tensions
from trajectory import inside_workspace

# Robot anchors
anchors = np.array([
    [-0.25, -0.235, 0.5],
    [ 0.25, -0.235, 0.5],
    [ 0.25,  0.235, 0.5],
    [-0.25,  0.235, 0.5]
])

m = 10
T_MAX = 60


def feasible_workspace():

    points = []

    xs = np.linspace(-0.23, 0.23, 25)
    ys = np.linspace(-0.23, 0.23, 25)
    zs = np.linspace(0.12, 0.43, 15)

    for x in xs:
        for y in ys:
            for z in zs:

                P = np.array([x, y, z])

                if not inside_workspace(P):
                    continue

                T = compute_tensions(P, anchors, m)

                if np.all(T > 0) and np.all(T < T_MAX):
                    points.append(P)

    return np.array(points)


# -----------------------------
# Visualization
# -----------------------------
if __name__ == "__main__":

    points = feasible_workspace()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(points[:,0], points[:,1], points[:,2], s=5)

    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")
    ax.set_title("Feasible Workspace of Cable Robot")

    plt.show()