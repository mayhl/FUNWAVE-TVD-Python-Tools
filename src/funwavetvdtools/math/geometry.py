


import numpy as np



def arctan2p(y, x):
    angles = np.arctan2(y, x)
    # Changing range from [-pi,pi] to [0,2 pi]
    angles[angles<0] += 2*np.pi
    return angles
 


def compute_angle_vectors(u, v):

    if type(u) is list: u = np.array(u)
    if type(v) is list: v = np.array(v)

    vm = np.linalg.norm(v)
    um = np.linalg.norm(u)
    num = np.dot(u,v)
    den = um*vm
    return np.arccos(num/den)


def order_vertices(x, y, x0=None, y0=None):

    if type(x) is list: x = np.array(x)
    if type(y) is list: y = np.array(y)

    nx = len(x)
    ny = len(y)


    if x0 is None or y0 is None:
        x0 = np.mean(x)
        y0 = np.mean(y)

    dx = x - x0
    dy = y - y0

    angles = arctan2p(dy, dx)
    idx = np.argsort(angles)

    return x[idx], y[idx]


def is_point_contain_convex_poly( x0, y0, x, y, tol=10**-6):

    if type(x) is list: x = np.array(x)
    if type(y) is list: y = np.array(y)

    # Checking if points is a vertice
    x_chk = np.abs(x - x0) < tol
    y_chk = np.abs(y - y0) < tol

    if np.any( x_chk & y_chk): return True

    n = len(x)

    x,y = order_vertices(x,y, x0, y0)

    vecs = [ [x[i] - x0, y[i] - y0 ] for i in range(n)]
    angles = [compute_angle_vectors(vecs[i-1], vecs[i]) for i in range(n)]

    return np.abs( 2*np.pi - np.sum(angles) ) < tol 
    
    


