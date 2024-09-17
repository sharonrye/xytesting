import positioner
import matplotlib.pyplot as plt
import numpy as np
import math
from math import pi, sqrt
from circle_fit import standardLSQ, hyperLSQ, hyperSVD


# generate fuzzy circles for testing Positioner class

def fuzzy_circle(center_x, center_y, radius, num_points):
    points = np.empty((num_points, 2))
    increment = 2 * pi / num_points
    for i in range(num_points):
        theta = i * increment
        x = radius * math.cos(theta) + center_x
        y = radius * math.sin(theta) + center_y
        np.append(points, [x, y])
    # adjust scale later
    fuzzer = np.random.normal(0, 0.1, (num_points, 2))
    points = points + fuzzer
    return points


def visualize(center_x, center_y, radius, num_points):
    points = fuzzy_circle(center_x, center_y, radius, num_points)
    circle = plt.Circle((center_x, center_y), radius, color='b', fill=False)
    ax = plt.gca()
    ax.add_patch(circle)
    ax.set_aspect('equal')
    plt.grid()
    plt.xticks(np.arange(-(radius + 1 + center_x), radius + 2 + center_x, 1))
    plt.yticks(np.arange(-(radius + 1 + center_y), radius + 2 + center_y, 1))
    for point in points:
        plt.plot(point[0], point[1], 'bo')


def fit_circle(points, fit_method='standardLSQ'):
    x_center, y_center, radius, sigma = None, None, None, None
    if fit_method == 'standardLSQ':
        x_center, y_center, radius, sigma = standardLSQ(points)
    elif fit_method == 'hyperLSQ':
        x_center, y_center, radius, sigma = hyperLSQ(points)
    elif fit_method == 'hyperSVD':
        x_center, y_center, radius, sigma = hyperSVD(points)

    return x_center, y_center, radius, sigma
