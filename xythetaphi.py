import math
from math import sqrt, degrees
import numpy as np
import matplotlib.pyplot as plt


# global threshold for checking equality
equality_threshold = 10 ** -6


def eq_thresh(a, b, thresh=equality_threshold):
    return abs(a - b) < thresh


def dist(x, y, a, b):
    return sqrt((x - a) ** 2 + (y - b) ** 2)


# given (x,y) coordinates and arm lengths r_theta and r_phi, computes and returns coordinates (x_0,y_0) the location
# of the phi motor (end of arm of length r_theta)
def xy_to_x0y0(x, y, r_theta, r_phi):
    if (x ** 2 + y ** 2) > (r_theta + r_phi) ** 2:
        print("(x,y) out of range")
        exit(1)
    # if (x,y) is on the edge of the circle, then the 2 arms are parallel
    if eq_thresh(dist(x, y, 0, 0), r_theta + r_phi, equality_threshold):
        theta = np.arccos(x / (r_theta + r_phi))
        return r_theta * np.cos(theta), r_theta * np.sin(theta)

    mag_xy = dist(x, y, 0, 0)
    # law of cosines
    sigma = np.arccos((mag_xy ** 2 + r_theta ** 2 - r_phi ** 2) / (2 * mag_xy * r_theta))
    d = r_theta * np.cos(sigma)
    k = sqrt(r_theta ** 2 - d ** 2)
    a = x / mag_xy * d
    b = y / mag_xy * d
    x_0 = (b * k / d) + a
    y_0 = b - (a * k / d)
    return x_0, y_0


# given coordinates (x,y) and arm lengths r_theta and r_phi, computes and returns (theta,phi)
def xy_to_thetaphi(x, y, r_theta, r_phi):
    # compute location of phi motor (x_0,y_0)
    x_0, y_0 = xy_to_x0y0(x, y, r_theta, r_phi)
    theta = np.arccos(x_0 / r_theta)
    # compute projection of phi arm onto theta arm
    dot = ((x - x_0) * x_0 + (y - y_0) * y_0)
    phi = np.arccos(dot / (r_phi * r_theta))
    # adjust theta to get signs to match up
    # quadrant 3
    if x_0 <= 0 and y_0 <= 0:
        theta = 2 * math.pi - theta
        pass
    # quadrant 4
    elif x_0 >= 0 and y_0 <= 0:
        theta = 2 * math.pi - theta
        pass

    return theta, phi


# given (theta,phi) and arm lengths r_theta and r_phi, computes coordinates (x,y) location of the end of the phi arm
def thetaphi_to_xy(theta, phi, r_theta, r_phi):
    # compute coordinates of (x_0,y_0) the end of the theta arm
    x_0 = np.cos(theta) * r_theta
    y_0 = np.sin(theta) * r_theta
    e = np.cos(phi) * r_phi
    f = np.sin(phi) * r_phi
    # add e to the vector in the direction of (x_0,y_0)
    x_1 = x_0 + e * x_0 / r_theta
    y_1 = y_0 + e * y_0 / r_theta
    # add f to the vector in the direction perpendicular to (x_1,y_1)
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


# given coordinates (x,y) and coordinates (x_0,y_0) of the location of the phi motor (end of arm of length r_theta) and
# arm lengths r_theta and r_phi, computes and returns alternative (theta,phi) and alternative coordinates (x_1,y_1)
# of the location of the phi motor
def alt_phi(x, y, x_0, y_0, r_theta, r_phi):
    # n is normalized vector (x, y)
    xy_norm = dist(x, y, 0, 0)
    # (x_n, y_n) is the unit vector in the direction of (x,y)
    x_n = x / xy_norm
    y_n = y / xy_norm
    # reflect across vector in the direction of (x_n,y_n)
    dot = x_0 * x_n + y_0 * y_n
    x_1 = x_0 - 2 * dot * x_n
    y_1 = y_0 - 2 * dot * y_n
    theta = np.arccos(x_1 / r_theta)
    # returns -x_1 and -y_1 to get signs to match up
    return theta, -r_phi, -x_1, -y_1


# theta and theta + 2 * pi represent the same angle
def alt_theta(theta):
    return theta + 2 * math.pi


def test_and_plot(x, y, r_theta, r_phi, theta_max=2 * math.pi, phi_max=math.pi):
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
    plt.plot((0, x_0), (0, y_0), label='theta arm')
    plt.plot((x_0, x), (y_0, y), label='phi arm')
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
        # plots alternative configuration with dotted lines
        plt.plot(x_n, y_n, 'o')
        plt.plot((0, x_n), (0, y_n), '--')
        plt.plot((x_n, x), (y_n, y), '--')
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    # test quadrant 1
    test_and_plot(-4, 4, 3.5, 5)
    # test quadrant 2
    test_and_plot(-3, -2, 2, 2.8)
    # test quadrant 3
    test_and_plot(3, -3, 4, 4)
    # test quadrant 4
    test_and_plot(4, 4, 3.5, 3)
    # test arms parallel
    test_and_plot(0, 3, 2, 1)
