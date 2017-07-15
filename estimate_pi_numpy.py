import time
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(int(time.time()))


def throws_in_circle(throws):
    return ((throws-0.5)**2).sum(axis=1) <= 0.5*0.5


def throw_n_darts(n):
    return np.random.uniform(0, 1, (n, 2))


def make_plot(in_circle, out_circle):
    plt.scatter(in_circle[:, 0], in_circle[:, 1], s=1)
    plt.scatter(out_circle[:, 0], out_circle[:, 1], s=1)
    plt.show()


def pi(n):
    throws = throw_n_darts(n)
    in_circle = throws_in_circle(throws)

    in_circle_throws = throws[in_circle]
    out_circle_throws = throws[~in_circle]

    pi_val = ((in_circle.sum())*4)/n
    print("Value if pi:", pi_val)

    make_plot(in_circle_throws, out_circle_throws)
    return pi_val


print(pi(100000))

