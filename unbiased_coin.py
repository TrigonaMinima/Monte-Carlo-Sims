import time
import random


random.seed(time.time())


def coin_toss():
    faces = ["heads", "tails"]
    toss = random.choice(faces)
    return toss


def gen_stats(outcomes):
    toss_stats = {
        "heads": 0,
        "tails": 0
        }

    for i in outcomes:
        toss_stats[i] += 1
    return toss_stats


def simulation_main(n):
    outcomes = [coin_toss() for i in range(n)]
    stats = gen_stats(outcomes)
    return stats


if __name__ == "__main__":
    import pandas as pd

    stats = []
    for i in range(1000):
        stats.append(simulation_main(i))

    a = pd.DataFrame(stats)
    a.to_csv("biased_coin.csv", index=False)

    # print(simulation_main(10000))

