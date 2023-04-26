import numpy as np


def linear_triangle_barycentric_weigths( xi, yi, x, y):

    x0, x1, x2 = x[0], x[1], x[2]
    y0, y1, y2 = y[0], y[1], y[2]

    den = (y2-y3)*(x1-x3) + (x3-x2)*(y1-y3)

    num = (y2-y3)*(xi-x3) + (x3-x2)*(yi-y3)
    w1 = num/den
    
    num = (y3-y1)*(xi-x3) + (x1-x3)*(yi-y3)
    w2 = num/den 
    
    w3 = 1 - w1-w2

    return [w1, w2, w3]


