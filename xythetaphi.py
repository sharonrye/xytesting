import math
from math import sqrt, degrees
import numpy as np
import matplotlib.pyplot as plt

# TODO: add greater range of motion for theta and phi
# TODO: generalize code to assume arms are NOT the same length
# center of positioner
# theta range approx 390
# phi range approx 190
# theta_max is hard stop
# phi_max is hard stop
# current position
# counterclockwise is positive


# global threshold for checking equality
equality_threshold = 10 ** -6


def eq_thresh(a, b, thresh=10 ** -6):
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


# TODO make cases for different quadrants
def thetaphi_to_xy(theta, phi, r):
    x_0 = np.cos(theta) * r
    y_0 = np.sin(theta) * r
    e = np.cos(phi)
    f = np.sin(phi) * r
    x_1 = x_0 * e + x_0
    y_1 = y_0 * e + y_0
    d = dist(-1 * y_1, x_1, 0, 0)
    x = f * -1 * y_1 / d + x_1
    y = f * x_1 / d + y_1
    return x, y


def dist(x, y, a, b):
    return sqrt((x - a) ** 2 + (y - b) ** 2)


def has_alternative(theta, phi, theta_max, phi_max):
    if 0 <= theta <= theta_max - 2 * math.pi:
        return True
    if 0 <= phi <= phi_max - math.pi:
        return True
    return False


# TODO: make cases for different quadrants
def alt_phi(x, y, x_0, y_0, r):
    # n is normalized vector (x, y)
    xy_norm = dist(x, y, 0, 0)
    x_n = x / xy_norm
    y_n = y / xy_norm
    dot = x_0 * x_n + y_0 * y_n
    x_1 = x_0 - 2 * dot * x_n
    y_1 = y_0 -2 * dot * y_n
    theta = np.arccos(x_1 / r)
    return theta, x_1, y_1


def alt_theta(theta):
    return theta + 2 * math.pi


def test_alts(x, y, x_0, y_0, r):
    phi_n, x_n, y_n = alt_phi(x, y, x_0, y_0, r)
    plt.plot(x_n, y_n, 'o')
    if eq_thresh(dist(x_n, y_n, 0, 0), r) and eq_thresh(dist(x, y, x_n, y_n), r):
        print('test_alts passes\n')


def test_xy_to_thetaphi(x, y, r, fig):
    # print(x_0, y_0)
    # print(dist(x_0, y_0, 0, 0))
    # print(dist(x_0, y_0, x, y))
    # print(degrees(theta), degrees(phi))
    pass



def test_thetaphi_to_xy(x, y, r, fig):
    theta, phi = xy_to_thetaphi(x, y, r)
    x_out, y_out = thetaphi_to_xy(theta, phi, r)
    if eq_thresh(x_out, x) and eq_thresh(y_out, y):
        print('(theta, phi) to (x,y) passes\n')
    # testing converting theta and phi back to x and y
    # x_1 = x_0 + np.cos(phi) * x_0
    # y_1 = y_0 + np.cos(phi) * y_0
    # plt.plot(x_1, y_1, 'o')

def test_all(x, y, r):
    x_0, y_0 = xy_to_x0y0(x, y, r)
    theta, phi = xy_to_thetaphi(x, y, r)
    plt.title('(x,y)=(' + str(x) + ',' + str(y) + '), r=' + str(r))
    plt.plot(0, 0, 'o')
    plt.plot(x, y, 'o')
    plt.plot(x_0, y_0, 'o')
    plt.plot((0, x_0), (0, y_0))
    plt.plot((x_0, x), (y_0, y))
    plt.xlim(-2 * r, 2 * r)
    plt.ylim(-2 * r, 2 * r)
    plt.grid(linestyle='--')
    plt.gca().set_aspect('equal')
    test_alts(x, y, x_0, y_0, r)
    plt.show()


class Positioner:
    def __init__(self, center, arm_length, theta_max, phi_max, current_x, current_y, current_theta, current_phi):
        self.arm_length = arm_length
        self.center = center
        self.theta_max = theta_max
        self.phi_max = phi_max
        self.current_x = current_x
        self.current_y = current_y
        self.current_theta = current_theta
        self.current_phi = current_phi
        self.moves = []

    def add_move(self, x, y):
        pass

    def log(self):
        pass


if __name__ == "__main__":
    test_all(4, 4, 3)
    # # test quadrant 1
    # test(-0.8, 0.4, 3)
    # # test quadrant 2
    # test(-0.4, -0.8, 3)
    # # test quadrant 3
    # test(0.8, -0.4, 3)
    # # test quadrant 4
    # test(0.4, 0.8, 3)
