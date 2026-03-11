import numpy as np

def trajectory(t):
    x = 0.1*np.sin(t)
    y = 0.1*np.cos(t)
    z = -0.3
    return np.array([x,y,z])