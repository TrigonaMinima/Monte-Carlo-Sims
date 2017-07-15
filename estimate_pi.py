import time
import random
import matplotlib.pyplot as plt

random.seed(time.time())


def dart_in_circle(x, y):
    """
    Circle is of radius 0.5 units. To check for the dart inside the circle
    we check with the following equation of circle:

    (x-x0)^2 + (y-y0)^2 <= r^2
    """
    if (x-0.5)*(x-0.5)+(y-0.5)*(y-0.5) <= 0.5*0.5:
        return True
    else:
        return False


def throw_darts():
    """
    Find random coordinates for the dart inside the square
    """
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    return x, y


def get_plot(a, b, c, d):
    plt.scatter(a, b, s=1)
    plt.scatter(c, d, s=1)
    plt.show()


def pi(n):
    """
    Estimate the value of pi by n experiments
    """
    in_circle_throws = 0

    in_circle_x = []
    in_circle_y = []

    out_circle_x = []
    out_circle_y = []

    for i in range(n):
        x, y = throw_darts()
        if dart_in_circle(x, y):
            in_circle_throws += 1
            in_circle_x.append(x)
            in_circle_y.append(y)
        else:
            out_circle_x.append(x)
            out_circle_y.append(y)

    get_plot(in_circle_x, in_circle_y, out_circle_x, out_circle_y)
    return (in_circle_throws*4/n)


print(pi(1000000))

