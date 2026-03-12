import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation

# -----------------------------
# 1. Anchor points
# -----------------------------
anchors = np.array([
    [-0.25, -0.25, 0.5],
    [ 0.25, -0.25, 0.5],
    [ 0.25,  0.25, 0.5],
    [-0.25,  0.25, 0.5]
])

# -----------------------------
# 2. Physical parameters
# -----------------------------
mass = 10      # kg
g = 9.81

F_gravity = np.array([0,0,-mass*g])

# -----------------------------
# 3. Workspace limits
# -----------------------------
workspace = {
    "xmin": -0.25,
    "xmax": 0.25,
    "ymin": -0.25,
    "ymax": 0.25,
    "zmin": 0.05,
    "zmax": 0.45
}

def limit_workspace(pos):
    x = np.clip(pos[0], workspace["xmin"], workspace["xmax"])
    y = np.clip(pos[1], workspace["ymin"], workspace["ymax"])
    z = np.clip(pos[2], workspace["zmin"], workspace["zmax"])
    return np.array([x,y,z])

# -----------------------------
# 4. Inverse kinematics
# -----------------------------
def inverse_kinematics(position, anchors):
    return np.linalg.norm(anchors - np.array(position), axis=1)

# -----------------------------
# 5. Cable directions
# -----------------------------
def cable_directions(pos, anchors):
    dirs = anchors - pos
    norms = np.linalg.norm(dirs, axis=1).reshape(-1,1)
    return dirs / norms

# -----------------------------
# 6. Tension estimation
# -----------------------------
def cable_tensions(mass, g):
    T = mass * g / 4
    return np.array([T, T, T, T])

# -----------------------------
# 7. Linear trajectory
# -----------------------------
def linear_trajectory(start, end, steps=80):
    return [np.array(start) + (np.array(end)-np.array(start))*t
            for t in np.linspace(0,1,steps)]

start_pos = [0,0,0.5]
end_pos   = [0,0,-0.5]

trajectory = linear_trajectory(start_pos,end_pos)

# -----------------------------
# 8. Cube vertices
# -----------------------------
def get_cube_vertices(center, size=0.05):

    x,y,z = center
    s = size/2

    corners = np.array([
        [x-s,y-s,z-s],
        [x+s,y-s,z-s],
        [x+s,y+s,z-s],
        [x-s,y+s,z-s],
        [x-s,y-s,z+s],
        [x+s,y-s,z+s],
        [x+s,y+s,z+s],
        [x-s,y+s,z+s]
    ])

    faces = [
        [corners[j] for j in [0,1,2,3]],
        [corners[j] for j in [4,5,6,7]],
        [corners[j] for j in [0,1,5,4]],
        [corners[j] for j in [2,3,7,6]],
        [corners[j] for j in [1,2,6,5]],
        [corners[j] for j in [4,7,3,0]]
    ]

    return faces

# -----------------------------
# 9. Figure setup
# -----------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim([-0.3,0.3])
ax.set_ylim([-0.3,0.3])
ax.set_zlim([0,0.6])

ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')


# anchors
ax.scatter(anchors[:,0],anchors[:,1],anchors[:,2],
           c='red',s=60,label='Anchors')

# initial cube
cube_faces = get_cube_vertices(trajectory[0])
cube_collection = Poly3DCollection(
    cube_faces,
    facecolors='cyan',
    edgecolors='black',
    alpha=0.7
)

ax.add_collection3d(cube_collection)

# cables
cables = [
    ax.plot([a[0],trajectory[0][0]],
            [a[1],trajectory[0][1]],
            [a[2],trajectory[0][2]],
            'k--')[0]
    for a in anchors
]

# text display
info_text = ax.text2D(0.02,0.95,'',transform=ax.transAxes)

# -----------------------------
# 10. Animation update
# -----------------------------
def update(frame):

    pos = limit_workspace(trajectory[frame])

    # update cube
    faces = get_cube_vertices(pos)
    cube_collection.set_verts(faces)

    # update cables
    for i,a in enumerate(anchors):

        cables[i].set_data([a[0],pos[0]],
                           [a[1],pos[1]])

        cables[i].set_3d_properties([a[2],pos[2]])

    # cable lengths
    lengths = inverse_kinematics(pos,anchors)

    # cable tensions
    tensions = cable_tensions(mass,g)

    # gravity arrow
    ax.quiver(pos[0],pos[1],pos[2],
              0,0,-1,
              length=0.12,
              color='red')

    # display values
    info_text.set_text(
        f"Position: {pos.round(3)}\n"
        f"Lengths (m): {lengths.round(3)}\n"
        f"Tensions (N): {tensions.round(1)}"
    )

    return cables + [cube_collection]

# -----------------------------
# 11. Run animation
# -----------------------------
ani = FuncAnimation(
    fig,
    update,
    frames=len(trajectory),
    interval=80,
    blit=False
)

plt.show()