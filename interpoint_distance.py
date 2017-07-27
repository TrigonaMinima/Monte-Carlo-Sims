#
# Average travel time b/w two points and the expressway
# There's a rectangle: R ≡ [0, 1] × [0, 0.6] (our universe)
# There's a circle with center 0 and radius 1/2 (out expressway)
# Traveling from A to B can either be direct or through expressway.
# Traveling time on expressway is negligible. The actual travel time is
# minimum of direct time and expressway time.
#

import sys
import numpy as np
import matplotlib.pyplot as plt


def get_closest_point(x, y):
    """
    Finds the intersetion point of the circle and the line between (0, 0) and (x, y).
    """
    slope = y / x
    x_close = (0.25 / (1 + slope * slope))**(0.5)
    y_close = slope * x_close
    return x_close, y_close


def in_circle(x, y):
    """
    Returns if the point is inside circle or not.
    """
    if x * x + y * y - 0.25 <= 0:
        return 1
    return 0


def get_interpoint_distance(ax, ay, bx, by):
    """
    Calculates the euclidian distance b/w 2 points.
    """
    distance = ((ax - bx)**2 + (ay - by)**2)**(0.5)
    return distance


def get_direct_time(ax, ay, bx, by):
    """
    Calculates the direct time taken from point a to b.
    """
    return (get_interpoint_distance(ax, ay, bx, by), ([ax, bx], [ay, by]))


def get_expressway_time(ax, ay, bx, by):
    """
    Calculates the time taken from point a to b if the expressway is presents.
    """
    a_in_circle = in_circle(ax, ay)
    b_in_circle = in_circle(bx, by)

    if a_in_circle and b_in_circle:
        points_x = [ax, bx]
        points_y = [ay, by]
        distance = 0
    elif a_in_circle:
        bx_close, by_close = get_closest_point(bx, by)
        points_x = [ax, bx_close, bx]
        points_y = [ay, by_close, by]
        distance = get_interpoint_distance(bx, by, bx_close, by_close)
    elif b_in_circle:
        ax_close, ay_close = get_closest_point(ax, ay)
        points_x = [ax, ax_close, bx]
        points_y = [ay, ay_close, by]
        distance = get_interpoint_distance(ax, ay, ax_close, ay_close)
    else:
        ax_close, ay_close = get_closest_point(ax, ay)
        bx_close, by_close = get_closest_point(bx, by)
        points_x = [ax, ax_close, bx_close, bx]
        points_y = [ay, ay_close, by_close, by]
        d1 = get_interpoint_distance(ax, ay, ax_close, ay_close)
        d2 = get_interpoint_distance(bx, by, bx_close, by_close)
        distance = d1 + d2

    return (distance, (points_x, points_y))


def actual_travel_time(ax, ay, bx, by):
    """
    Returns the minimum of the 2 times - direct or expressway.
    """
    td, points = get_direct_time(ax, ay, bx, by)
    te, points = get_expressway_time(ax, ay, bx, by)
    if td > te:
        return (te, points, "e")
    return(td, points, "d")
    # return min(td, te)


def simulation(a, b):
    """
    Runs the simulation for a set of starting and ending positions.
    """
    times = []
    points = []
    time_type = []

    for ai, bi in zip(a, b):
        time, pts, tt = actual_travel_time(*ai, *bi)
        times.append(time)
        points.append(pts)
        time_type.append(tt)

    return np.array(times), points, time_type


def average_time(times):
    """
    Returns the average of all the times for all the set of start and ending
    positions.
    """
    return times.mean()


def draw(ax, bx, ay, by, path_points):
    """
    Draws the whole flow trace.
    """
    circle = plt.Circle((0, 0), 0.5, color='black', fill=0)
    rectangle = plt.Rectangle((0, 0), 1, 0.6, color='black', fill=0)
    plt.gca().add_artist(circle)
    plt.gca().add_artist(rectangle)

    # draw points
    for xi, yi in zip(zip(ax, bx), zip(ay, by)):
        plt.scatter(xi, yi, s=6)

    for xi, yi in path_points:
        plt.plot(xi, yi)

    plt.show()


def init(num):
    """
    Returns the "num" number of starting and ending positions.
    """
    ax = np.random.uniform(0, 1, num)
    bx = np.random.uniform(0, 1, num)
    ay = np.random.uniform(0, 0.6, num)
    by = np.random.uniform(0, 0.6, num)

    return ax, ay, bx, by


if __name__ == "__main__":
    scenario = sys.argv[-1]

    if scenario == "1":
        ax = [0.45, 0.04, 0.56, 0.20, 0.54, 0.00]
        ay = [0.05, 0.13, 0.49, 0.30, 0.30, 0.00]
        bx = [0.05, 0.18, 0.16, 0.95, 0.40, 0.60]
        by = [0.45, 0.32, 0.50, 0.40, 0.59, 0.45]
        times, path_points, time_type = simulation(zip(ax, ay), zip(bx, by))
        print(times, time_type)
        print(path_points)
        print("Average distance:", average_time(times))
        draw(ax, bx, ay, by, path_points)
    elif scenario == "2":
        ax, ay, bx, by = init(20)
        times, path_points, time_type = simulation(zip(ax, ay), zip(bx, by))
        print("Average distance:", average_time(times))
        draw(ax, bx, ay, by, path_points)
