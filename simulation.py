from trajectory import trajectory
from inverse_kinematics import cable_lengths

def simulate(t):
    P = trajectory(t)
    L = cable_lengths(P)
    
    return P, L