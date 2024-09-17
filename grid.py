import math
import numpy as np
import matplotlib.pyplot as plt

"""Creates grid of target points for XY tests of fiber positioners"""

ieos_a000328 = [1, 5, 13, 29, 49, 81, 113, 149, 197, 253, 317, 377, 441, 529, 613, 709, 797, 901, 1009, 1129, 1257,
                1373, 1517, 1653, 1793, 1961, 2121, 2289, 2453, 2629, 2821, 3001, 3209, 3409, 3625, 3853, 4053, 4293,
                4513, 4777, 5025, 5261, 5525, 5789, 6077, 6361, 6625]


def standard_grid(num_points, r_theta, r_phi, center_x, center_y):
    """Given the arm lengths r_theta, r_phi and the center of a positioner, return a list of numpoints many
    (x,y) coordinates spaced evenly within the span of the two arms."""
    r = r_theta + r_phi
    index = np.searchsorted(ieos_a000328, num_points)
    unit = r / index
    square = []
    for x in range(-index, index + 1, 1):
        for y in range(-index, index + 1, 1):
            square.append((x * unit + center_x, y * unit + center_y, (x * unit) ** 2 + (y * unit) ** 2))
    # throw out points outside the circle
    circ = []
    for point in square:
        if point[2] <= r ** 2:
            circ.append(point)
    # throw out extraneous points if any, starting with the points closest to the edge
    circ = np.asarray(circ)
    circ = sorted(circ, key=lambda a: a[2])
    return circ[0:num_points]


def outer_edge_grid(numpoints, r_theta, r_phi, center):
    """Given the arm lengths r_theta, r_phi and the center of a positioner, return a list of numpoints many
    (x,y) coordinates at the outer edge of the range of the phi motor."""
    pass


def inner_edge_grid(numpoints, r_theta, r_phi, center):
    """Given the arm lengths r_theta, r_phi and the center of a positioner, return a list of numpoints many
    (x,y) coordinates at the inner edge of the range of the phi motor."""
    pass


def random_grid(numpoints, r_theta, r_phi, center):
    """Given the arm lengths r_theta, r_phi and the center of a positioner, return a list of numpoints many
    (x,y) coordinates picked uniformly at random within the span of the two arms."""
    pass


def standard_random(numpoints, r_theta, r_phi, center):
    pass
