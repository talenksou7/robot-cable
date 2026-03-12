import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from simulation import simulate  # Your simulate(t) returns P, L, T, warnings

# Robot anchors
anchors = np.array([
    [-0.25, -0.235, 0.5],
    [ 0.25, -0.235, 0.5],
    [ 0.25,  0.235, 0.5],
    [-0.25,  0.235, 0.5]
])

T_MAX = 60  # Max allowable cable tensionclear

# -----------------------------
# Setup figure
# -----------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-0.3, 0.3])
ax.set_ylim([-0.28, 0.28])
ax.set_zlim([0, 0.55])
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.set_title('Cable-Driven Robot Visualization')

# Plot anchors
ax.scatter(anchors[:,0], anchors[:,1], anchors[:,2], color='k', s=50, label='Anchors')

# Platform plot
platform_plot, = ax.plot([], [], [], 'o', color='orange', markersize=8, label='Platform')

# Cable lines
cable_lines = [ax.plot([], [], [], 'b')[0] for _ in range(4)]

# -----------------------------
# Animation function
# -----------------------------
def animate(frame):
    t = frame / 10.0  # time scaling
    P, L, T, warnings = simulate(t)
    
    # Update platform position (must be sequences)
    platform_plot.set_data([P[0]], [P[1]])
    platform_plot.set_3d_properties([P[2]])
    
    # Update cables
    for i in range(4):
        xs = [anchors[i,0], P[0]]
        ys = [anchors[i,1], P[1]]
        zs = [anchors[i,2], P[2]]
        cable_lines[i].set_data(xs, ys)
        cable_lines[i].set_3d_properties(zs)
        
        # Color based on tension
        if T[i] > T_MAX:
            cable_lines[i].set_color('r')      # tension too high
        elif T[i] < 0:
            cable_lines[i].set_color('gray')   # slack
        else:
            cable_lines[i].set_color('b')      # normal

    return [platform_plot] + cable_lines

# -----------------------------
# Run animation
# -----------------------------
anim = FuncAnimation(fig, animate, frames=500, interval=50, blit=False)
plt.legend()
plt.show()