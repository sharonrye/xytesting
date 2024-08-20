import math
from math import sqrt, degrees
import numpy as np
import matplotlib.pyplot as plt

# TODO: generalize code to assume arms are NOT the same length
# TODO: add Positioner class, should contain:
# center of positioner
# theta range approx 390
# phi range approx 190
# theta_max is hard stop
# phi_max is hard stop
# current position
# counterclockwise is positive


# global threshold for checking equality
equality_threshold = 10 ** -6


def eq_thresh(a, b, thresh=equality_threshold):
    return abs(a - b) < thresh


def dist(x, y, a, b):
    return sqrt((x - a) ** 2 + (y - b) ** 2)


def xy_to_x0y0(x, y, r_theta, r_phi):
    if (x ** 2 + y ** 2) > (r_theta + r_phi) ** 2:
        print("(x,y) out of range")
        exit(-1)
    # if (x,y) is on the edge of the circle, then the 2 arms are parallel
    if eq_thresh(dist(x, y, 0, 0), r_theta + r_phi, equality_threshold):
        theta = np.arccos(x / (r_theta + r_phi))
        return r_theta * np.cos(theta), r_theta * np.sin(theta)

    mag_xy = dist(x, y, 0, 0)
    # law of cosines
    temp = (mag_xy ** 2 + r_theta ** 2 - r_phi ** 2) / 2 * mag_xy * r_theta
    sigma = np.arccos((mag_xy ** 2 + r_theta ** 2 - r_phi ** 2) / (2 * mag_xy * r_theta))
    d = r_theta * np.cos(sigma)
    k = sqrt(r_theta ** 2 - d ** 2)
    a = x / mag_xy * d
    b = y / mag_xy * d
    x_0 = (b * k / d) + a
    y_0 = b - (a * k / d)
    return x_0, y_0


def xy_to_thetaphi(x, y, r_theta, r_phi):
    x_0, y_0 = xy_to_x0y0(x, y, r_theta, r_phi)
    theta = np.arccos(x_0 / r_theta)
    dot = ((x - x_0) * x_0 + (y - y_0) * y_0)
    phi = np.arccos(dot / (r_phi * r_theta))
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
def thetaphi_to_xy(theta, phi, r_theta, r_phi):
    x_0 = np.cos(theta) * r_theta
    y_0 = np.sin(theta) * r_theta
    e = np.cos(phi) * r_phi
    f = np.sin(phi) * r_phi
    x_1 = x_0 + e * x_0 / r_theta
    y_1 = y_0 + e * y_0 / r_theta
    d = dist(-1 * y_1, x_1, 0, 0)
    x = f * -1 * y_1 / d + x_1
    y = f * x_1 / d + y_1
    return x, y


def has_alternative(theta, phi, theta_max, phi_max):
    if 0 <= theta <= theta_max - 2 * math.pi:
        return True
    if 0 <= phi <= phi_max - math.pi:
        return True
    return False


# TODO: make cases for different quadrants
def alt_phi(x, y, x_0, y_0, r_theta, r_phi):
    # n is normalized vector (x, y)
    xy_norm = dist(x, y, 0, 0)
    # (x_n, y_n) is the unit vector in the direction of (x,y)
    x_n = x / xy_norm
    y_n = y / xy_norm
    dot = x_0 * x_n + y_0 * y_n
    x_1 = x_0 - 2 * dot * x_n
    y_1 = y_0 - 2 * dot * y_n
    theta = np.arccos(x_1 / r_theta)
    return theta, -r_phi, -x_1, -y_1


def alt_theta(theta):
    return theta + 2 * math.pi


def test_and_plot(x, y, r_theta, r_phi):
    r = max(r_theta, r_phi)
    x_0, y_0 = xy_to_x0y0(x, y, r_theta, r_phi)
    # check to make sure (x_0,y_0) r_theta away from (0,0) and r_phi away from (x,y)
    if eq_thresh(dist(x_0, y_0, 0, 0), r_theta) and eq_thresh(dist(x_0, y_0, x, y), r_phi):
        print('(x,y) to (x_0,y_0) passed')
    else:
        print('(x,y) to (x_0,y_0) failed')
        exit(1)
    theta, phi = xy_to_thetaphi(x, y, r_theta, r_phi)
    x_out, y_out = thetaphi_to_xy(theta, phi, r_theta, r_phi)
    # check to make sure (x_out,y_out) is equal to (x,y)
    if eq_thresh(x_out, x) and eq_thresh(y_out, y):
        print('(theta,phi) to (x,y) passed')
    else:
        print('(theta,phi) to (x,y) failed')
        exit(1)
    # plot arms
    plt.title('(x,y)=(' + str(x) + ',' + str(y) + '), r_theta=' + str(r_theta) + ', r_phi=' + str(r_phi))
    plt.plot(0, 0, 'o')
    plt.plot(x, y, 'o')
    plt.plot(x_0, y_0, 'o')
    plt.plot((0, x_0), (0, y_0))
    plt.plot((x_0, x), (y_0, y))
    plt.xlim(-2 * r, 2 * r)
    plt.ylim(-2 * r, 2 * r)
    plt.grid(linestyle='--')
    plt.gca().set_aspect('equal')
    # TODO: check if alternative configuration exists (for now set to True)
    if True:
        # compute alternative angle
        theta_n, phi_n, x_n, y_n = alt_phi(x, y, x_0, y_0, r_theta, r_phi)
        # check that (x_n,y_n) is r_theta away from (0,0) and r_phi away from (x,y)
        if eq_thresh(dist(x_n, y_n, 0, 0), r_theta) and eq_thresh(dist(x_n, y_n, x, y), r_phi):
            print('alternative config passed')
        else:
            print('alternative config failed')
            exit(1)
        plt.plot(x_n, y_n, 'o')
        plt.plot((0, x_n), (0, y_n), '--')
        plt.plot((x_n, x), (y_n, y), '--')
    plt.show()


# TODO: add state and logging for Positioner class
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
    test_and_plot(4, 4, 3, 5)
    # # test quadrant 1
    # test_and_plot(-0.8, 0.4, 3)
    # # test quadrant 2
    # test_and_plot(-0.4, -0.8, 3)
    # # test quadrant 3
    # test_and_plot(0.8, -0.4, 3)
    # # test quadrant 4
    # test_and_plot(0.4, 0.8, 3)
