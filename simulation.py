from trajectory import trajectory, inside_workspace
from inverse_kinematics import cable_lengths
from tension_solver import compute_tensions
import numpy as np

# Robot parameters
anchors = np.array([
    [-0.25, -0.235, 0.5],
    [ 0.25, -0.235, 0.5],
    [ 0.25,  0.235, 0.5],
    [-0.25,  0.235, 0.5]
])
m = 10          # platform mass (kg)
T_MAX = 60      # max cable tension (N)

def simulate(t):
    # Get platform position from trajectory
    P = trajectory(t)
    
    # Safety check: keep inside workspace
    if not inside_workspace(P):
        P = np.clip(P, [-0.25, -0.235, 0.1], [0.25, 0.235, 0.45])
    
    # Compute cable lengths
    L = cable_lengths(P)
    
    # Compute cable tensions
    T = compute_tensions(P, anchors, m)
    
    # Check for slack or overloaded cables
    warnings = []
    if np.any(T < 0):
        warnings.append("Slack cable detected!")
    if np.any(T > T_MAX):
        warnings.append("Tension exceeds max limit!")
    
    return P, L, T, warnings