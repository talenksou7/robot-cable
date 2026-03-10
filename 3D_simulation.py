import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation

# --- 1. Anchor points ---
anchors = np.array([
    [-0.25, -0.25, 0.5],
    [ 0.25, -0.25, 0.5],
    [ 0.25,  0.25, 0.5],
    [-0.25,  0.25, 0.5]
])

# --- 2. Inverse kinematics ---
def inverse_kinematics(position, anchors):
    return np.linalg.norm(anchors - np.array(position), axis=1)

# --- 3. Linear trajectory ---
def linear_trajectory(start, end, steps=50):
    return [np.array(start) + (np.array(end) - np.array(start)) * t for t in np.linspace(0, 1, steps)]

# --- 4. Cube vertices ---
def get_cube_vertices(center, size=0.05):
    x, y, z = center
    s = size/2
    corners = np.array([
        [x-s, y-s, z-s],
        [x+s, y-s, z-s],
        [x+s, y+s, z-s],
        [x-s, y+s, z-s],
        [x-s, y-s, z+s],
        [x+s, y-s, z+s],
        [x+s, y+s, z+s],
        [x-s, y+s, z+s]
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

# --- 5. Trajectory ---
start_pos = [0, 0, 0.3]
end_pos   = [0.1, 0.1, 0.35]
trajectory = linear_trajectory(start_pos, end_pos, steps=50)

# --- 6. Setup figure ---
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-0.3,0.3])
ax.set_ylim([-0.3,0.3])
ax.set_zlim([0,0.6])
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
ax.set_title('Cable Robot Kinematics Animation')

# plot anchors
ax.scatter(anchors[:,0], anchors[:,1], anchors[:,2], c='r', s=50, label='Anchors')

# initial cube
cube_faces = get_cube_vertices(trajectory[0])
cube_collection = Poly3DCollection(cube_faces, facecolors='cyan', edgecolors='k', alpha=0.6)
ax.add_collection3d(cube_collection)

# initial cables
cables = [ax.plot([a[0], trajectory[0][0]], 
                  [a[1], trajectory[0][1]], 
                  [a[2], trajectory[0][2]], 'k--')[0] for a in anchors]

# text for cable lengths
length_text = ax.text2D(0.02, 0.95, '', transform=ax.transAxes)

# --- 7. Animation function ---
def update(frame):
    pos = trajectory[frame]
    # update cube
    faces = get_cube_vertices(pos)
    cube_collection.set_verts(faces)
    # update cables
    for i, a in enumerate(anchors):
        cables[i].set_data([a[0], pos[0]], [a[1], pos[1]])
        cables[i].set_3d_properties([a[2], pos[2]])
    # compute and display cable lengths
    lengths = inverse_kinematics(pos, anchors)
    length_text.set_text(f"Cable lengths (m): {lengths.round(3)}")
    return cables + [cube_collection, length_text]

# --- 8. Run animation (display only) ---
ani = FuncAnimation(fig, update, frames=len(trajectory), interval=100, blit=False)

plt.show()  # <-- just display the animation