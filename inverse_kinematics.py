import numpy as np

# anchor points of the robot
A1 = np.array([-0.25, -0.235, 0.5])
A2 = np.array([ 0.25, -0.235, 0.5])
A3 = np.array([ 0.25,  0.235, 0.5])
A4 = np.array([-0.25,  0.235, 0.5])

def cable_lengths(P):
    L1 = np.linalg.norm(P - A1)
    L2 = np.linalg.norm(P - A2)
    L3 = np.linalg.norm(P - A3)
    L4 = np.linalg.norm(P - A4)
    
    return np.array([L1, L2, L3, L4])