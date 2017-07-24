#
# Nagel−Schreckenberg traffic
# Assumption: The road is a circle.
#

import random
import numpy as np
import matplotlib.pyplot as plt


vehicles = 250
road_zones = 1000
v_max = 5
slowing_chance = 1 / 3
iterations = 1000
burn_in_iters = 2500

# vehicles = 10
# road_zones = 100
# v_max = 5
# slowing_chance = 1 / 3
# iterations = 10
# burn_in_iters = 10


def init():
    """
    Generating the random starting positions of the vehicles. Initializing the
    starting velocities to 0.
    """
    starting_pos = np.msort(np.random.choice(
        range(road_zones), vehicles, replace=0))
    starting_vel = np.zeros(vehicles, int)
    print("Initialization complete...")
    return (starting_pos, starting_vel)


def car_pos(old_pos, new_vel):
    """
    Determining the new position of the vehicle.
    """
    new_pos = old_pos + new_vel
    if new_pos >= road_zones:
        new_pos -= road_zones
    return new_pos


def separation(car_pos, front_car_pos):
    """
    Determining the separation b/w current car and the next car.
    """
    d = front_car_pos - car_pos + 1
    # if front_car_pos > car_pos:
    #     d = front_car_pos - car_pos + 1
    # else:
    #     d = car_pos - front_car_pos + 1
    return d


def car_velocity(old_vel, d):
    """
    Determining the new velocity of the car.
    """
    new_vel = min(old_vel + 1, v_max)
    new_vel = min(new_vel, d - 1)

    slow_flag = random.choices(
        [0, 1], [1 - slowing_chance, slowing_chance], k=1)[0]
    if slow_flag and new_vel > 0:
        new_vel = max(0, new_vel - 1)

    return new_vel


def one_iteration(all_pos, all_vel):
    """
    Runs one iteration of the simulation
    When the last vehicle is being considered. it has to be rotated.
    """
    all_new_positions = []
    all_new_velocities = []
    # max_pos = max(all_pos)
    for i, (pos, vel) in enumerate(zip(all_pos, all_vel)):
        if (i == vehicles - 1):
            d = separation(pos, (all_pos[0] + road_zones))
        elif pos > all_pos[i + 1]:
            d = separation(pos, (all_pos[i + 1] + road_zones))
        else:
            d = separation(pos, all_pos[i + 1])

        new_vel = car_velocity(vel, d)
        new_pos = car_pos(pos, new_vel)

        all_new_velocities.append(new_vel)
        all_new_positions.append(new_pos)

    return all_new_positions, all_new_velocities


def burn_in(all_pos, all_vel):
    """
    The burn-in period
    """
    for i in range(burn_in_iters):
        all_new_positions, all_new_velocities = one_iteration(all_pos, all_vel)

    print("Burn-in period over (%d iterations)..." % burn_in_iters)
    return all_new_positions, all_new_velocities


def simulation():
    """
    main function which executes the simulation
    """
    pos_matrix = []
    vel_matrix = []

    all_pos, all_vel = init()

    # burn-in paeriod
    all_new_positions, all_new_velocities = burn_in(all_pos, all_vel)

    all_new_positions, all_new_velocities = one_iteration(all_pos, all_vel)
    for i in range(iterations):
        pos_matrix.append(all_new_positions)
        vel_matrix.append(all_new_velocities)
        all_new_positions, all_new_velocities = one_iteration(
            all_new_positions, all_new_velocities)

    all_velocities = np.array(vel_matrix)
    all_positions = np.array(pos_matrix)

    print("Simulation complete (%d iterations)..." % iterations)
    # print("Velocities:\n", all_velocities)
    # print("Positions:\n", all_positions)
    return all_velocities, all_positions


def positions_plot(all_pos):
    """
    Plots the positions to observe the pattern.
    """
    print("Generating plot...")
    for index, x in enumerate(all_pos):
        y = np.full(vehicles, (iterations - index), int)
        y = y + np.random.uniform(0, 0.5, vehicles)
        plt.scatter(x, y, s=0.03, color='black')

    plt.show()


if __name__ == '__main__':
    all_vel, all_pos = simulation()
    positions_plot(all_pos)
