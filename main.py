import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

anchors = np.array([
    [-0.25, -0.25, 0.5],
    [ 0.25, -0.25, 0.5],
    [ 0.25,  0.25, 0.5],
    [-0.25,  0.25, 0.5]
])

def inverse_kinematics(position, anchors):
    x, y, z = position
    lengths = np.linalg.norm(anchors - np.array([x, y, z]), axis=1)
    return lengths

# --- 3. Define a simple linear trajectory ---
def linear_trajectory(start, end, steps=10):
    return [np.array(start) + (np.array(end) - np.array(start)) * t for t in np.linspace(0, 1, steps)]

# --- 4. Trajectory positions ---
start_pos = [0, 0, 0.3]   # starting platform center
end_pos   = [0.1, 0.1, 0.35] # end platform center
trajectory = linear_trajectory(start_pos, end_pos, steps=20)

# --- 5. Compute cable lengths for each position ---
all_lengths = []
for pos in trajectory:
    lengths = inverse_kinematics(pos, anchors)
    all_lengths.append(lengths)
    print(f"Platform at {pos} → Cable lengths: {lengths}")

# --- 6. 3D Visualization ---
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot anchors
ax.scatter(anchors[:,0], anchors[:,1], anchors[:,2], c='r', s=50, label='Anchors')

# Plot platform positions and cables
for pos in trajectory:
    # Platform center
    ax.scatter(pos[0], pos[1], pos[2], c='b')
    # Draw cables
    for a in anchors:
        ax.plot([a[0], pos[0]], [a[1], pos[1]], [a[2], pos[2]], 'k--', linewidth=0.8)

ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.set_zlabel('Z [m]')
ax.set_title('Cable Robot Kinematics Simulation')
ax.set_xlim([-0.3, 0.3])
ax.set_ylim([-0.3, 0.3])
ax.set_zlim([0, 0.6])
ax.legend()
plt.show()