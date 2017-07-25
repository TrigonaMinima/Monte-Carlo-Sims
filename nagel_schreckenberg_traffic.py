#
# Nagel−Schreckenberg traffic
# Assumption: The road is a circle.
#

import sys
import random
import numpy as np
import matplotlib.pyplot as plt


verbosity = 1
vehicles = 100
road_zones = 1000
v_max = 5
slowing_chance = 1 / 3
iterations = 1000
burn_in_iters = 2500


def init(mode='r'):
    """
    Generating the starting positions of the vehicles. Initializing the
    starting velocities to 0.

    mode: 'r', 'e', or 'fk' (random, equidistant, first k positions)
    """
    starting_vel = np.zeros(vehicles, int)

    if mode == 'r':
        starting_pos = np.msort(np.random.choice(
            range(road_zones), vehicles, replace=0))
    elif mode == 'e':
        step = road_zones // vehicles
        # print(step)
        starting_pos = np.arange(0, road_zones, step)[:vehicles]
    elif mode == 'fk':
        starting_pos = np.arange(vehicles)

    # print(starting_pos)

    if verbosity:
        print("Initialization complete...")
    return (starting_pos, starting_vel)


def separation(index, position, all_positions):
    """
    Determining the separation b/w current car and the next car.
    """
    car_pos = position
    if (index == vehicles - 1):
        front_car_pos = (all_positions[0] + road_zones)
    elif car_pos > all_positions[index + 1]:
        front_car_pos = (all_positions[index + 1] + road_zones)
    else:
        front_car_pos = all_positions[index + 1]

    d = front_car_pos - (car_pos + 1)
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


def car_pos(old_pos, new_vel):
    """
    Determining the new position of the vehicle.
    """
    new_pos = old_pos + new_vel
    if new_pos >= road_zones:
        new_pos -= road_zones
    return new_pos


def one_iteration(all_pos, all_vel):
    """
    Runs one iteration of the simulation
    When the last vehicle is being considered. it has to be rotated.
    """
    all_new_positions = []
    all_new_velocities = []
    for i, (pos, vel) in enumerate(zip(all_pos, all_vel)):
        d = separation(i, pos, all_pos)
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

    if verbosity:
        print("Burn-in period over (%d iterations)..." % burn_in_iters)
    return all_new_positions, all_new_velocities


def simulation(init_mode='r'):
    """
    Main function which executes the simulation
    """
    pos_matrix = []
    vel_matrix = []

    all_pos, all_vel = init(init_mode)

    # burn-in period
    all_new_positions, all_new_velocities = burn_in(all_pos, all_vel)

    all_new_positions, all_new_velocities = one_iteration(all_pos, all_vel)
    for i in range(iterations):
        pos_matrix.append(all_new_positions)
        vel_matrix.append(all_new_velocities)
        all_new_positions, all_new_velocities = one_iteration(
            all_new_positions, all_new_velocities)

    all_velocities = np.array(vel_matrix)
    all_positions = np.array(pos_matrix)

    if verbosity:
        print("Simulation complete (%d iterations)..." % iterations)
        # print("Velocities:\n", all_velocities)
        # print("Positions:\n", all_positions)
    return all_velocities, all_positions


def total_distance_travelled(all_positions):
    return all_positions.sum()


def flow_trace(all_pos):
    """
    Plots the positions to observe the pattern.
    """
    print("Generating plot...")
    for index, x in enumerate(all_pos):
        y = np.full(vehicles, (iterations - index), int)
        y = y + np.random.uniform(0, 0.5, vehicles)
        plt.scatter(x, y, s=0.03, color='black')
    plt.show()


def fundamental_diagram(vehicles_n, distances_d):
    plt.scatter(distances_d, vehicles_n)
    plt.show()


if __name__ == '__main__':
    """
    1. Single run of the simulation
    2 (a). Multiple runs of the simulation
    3 (b). Multiple runs of the simulation
    4. Different starting positions
    """

    scenario = sys.argv[-1]
    if scenario == '1':
        print("SCENARIO 1")
        vehicles = 50
        road_zones = 1000
        v_max = 5
        slowing_chance = 1 / 3
        iterations = 1000
        burn_in_iters = 1000

        all_vel, all_pos = simulation(init_mode='e')
        flow_trace(all_pos)
        print(total_distance_travelled(all_pos))
    if scenario == '2':
        print("SCENARIO 2")
        road_zones = 1000
        v_max = 5
        slowing_chance = 1 / 3
        iterations = 1000
        burn_in_iters = 1000
        verbosity = 0

        vehicles_n = []
        distances_d = []
        for i, num in enumerate(range(55, 500, 5)):
            vehicles = num
            vehicles_n.append(num)
            all_vel, all_pos = simulation(init_mode='e')
            distances_d.append(total_distance_travelled(all_pos))

            print(i, end="..")
            sys.stdout.flush()

        fundamental_diagram(vehicles_n, distances_d)
    else:
        print("DEFAULT SCENARIO")
        all_vel, all_pos = simulation(init_mode='e')
        flow_trace(all_pos)
