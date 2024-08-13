import math
from math import sqrt, degrees
import numpy as np
import matplotlib.pyplot as plt

# global threshold for checking equality
equality_threshold = 10 ** -6


def eq_thresh(a, b, thresh):
    return abs(a - b) < thresh


def xy_to_x0y0(x, y, r):
    if (x ** 2 + y ** 2) > 4 * r ** 2:
        print("(x,y) out of range")
        exit(-1)
    # if (x,y) is on the edge of the circle, then the 2 arms are parallel
    if eq_thresh(dist(x, y, 0, 0), 2 * r, equality_threshold):
        return x / 2, y / 2

    a = float(x) / 2
    b = float(y) / 2
    d = sqrt(a ** 2 + b ** 2)
    k = sqrt(r ** 2 - d ** 2)
    x_0 = (b * k / d) + a
    y_0 = b - (a * k / d)
    # alternative way of computing
    # m = -1 * float(x) / float(y)
    # x_0 = sqrt(k ** 2/ (1 + m ** 2)) + a
    # y_0 = m * (x_0 - a) + b
    return x_0, y_0


def xy_to_thetaphi(x, y, r):
    x_0, y_0 = xy_to_x0y0(x, y, r)
    theta = np.arccos(x_0 / r)
    dot = ((x - x_0) * x_0 + (y - y_0) * y_0)
    phi = np.arccos(dot / r ** 2)
    # quadrant 1
    if x_0 >= 0 and y_0 >= 0:
        # theta remains unchanged
        pass
    # quadrant 2
    elif x_0 <= 0 and y_0 >= 0:
        # theta remains unchanged
        pass
    # quadrant 3
    elif x_0 <= 0 and y_0 <= 0:
        theta = 2 * math.pi - theta
        pass
    # quadrant 4
    elif x_0 >= 0 and y_0 <= 0:
        theta = 2 * math.pi - theta
        pass

    return theta, phi


def dist(x, y, a, b):
    return sqrt((x - a) ** 2 + (y - b) ** 2)

def test(x, y, r):
    x_0, y_0 = xy_to_x0y0(x, y, r)
    theta, phi = xy_to_thetaphi(x, y, r)
    print(x_0, y_0)
    print(dist(x_0, y_0, 0, 0))
    print(dist(x_0, y_0, x, y))
    print(degrees(theta), degrees(phi))
    plt.plot(0, 0, 'o')
    plt.plot(x, y, 'o')
    plt.plot(x_0, y_0, 'o')
    plt.plot((0, x_0), (0, y_0))
    plt.plot((x_0, x), (y_0, y))
    plt.xlim(-2 * r, 2 * r)
    plt.ylim(-2 * r, 2 * r)
    plt.grid(linestyle='--')
    plt.show()

if __name__ == "__main__":
    # test quadrant 1
    test(-0.8, 0.4, 3)
    # test quadrant 2
    test(-0.4, -0.8, 3)
    # test quadrant 3
    test(0.8, -0.4, 3)
    # test quadrant 4
    test(0.4, 0.8, 3)

