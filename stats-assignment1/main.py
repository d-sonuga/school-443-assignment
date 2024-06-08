import numpy as np
from scipy.stats import norm


def calc_z_score(x):
    mean, std_dev = 1640, 62
    return (x - mean) / std_dev

def classwork_answers():
    greater_than_1800 = 1 - norm.cdf(calc_z_score(1800))
    lesser_than_1550 = norm.cdf(calc_z_score(1550))
    between_1600_and_1700 = norm.cdf(calc_z_score(1700)) - norm.cdf(calc_z_score(1600))
    print("No Simulation:")
    print("-------------")
    print(f"Estimated probability that the bulb will have "
        f"a brightness greater than 1800 lumens: {greater_than_1800:.4f}")
    print(f"Estimated probability that the bulb will have "
        f"a brightness lesser than 1550 lumens: {lesser_than_1550:.4f}")
    print(f"Estimated probability that the bulb will have "
        f"a brightness between 1600 and 1700 lumens: {between_1600_and_1700:.4f}")
    print()

def simulation():
    sample_size, no_of_sims = 700, 100
    mean, std_dev = 1640, 62
    no_greater_than_1800 = 0
    no_lesser_than_1550 = 0
    no_between_1600_and_1700 = 0

    for _ in range(no_of_sims):
        sample = np.random.normal(mean, std_dev, sample_size)
        no_greater_than_1800 += (sample > 1800).sum()
        no_lesser_than_1550 += (sample < 1550).sum()
        no_between_1600_and_1700 += (sample < 1700).sum() - (sample < 1600).sum()
    
    greater_than_1800 = no_greater_than_1800 / (sample_size * no_of_sims)
    lesser_than_1550 = no_lesser_than_1550 / (sample_size * no_of_sims)
    between_1600_and_1700 = no_between_1600_and_1700 / (sample_size * no_of_sims)

    print("Simulation:")
    print("-----------")
    print(f"Estimated probability that the bulb will have "
        f"a brightness greater than 1800 lumens: {greater_than_1800:.4f}")
    print(f"Estimated probability that the bulb will have "
        f"a brightness lesser than 1550 lumens: {lesser_than_1550:.4f}")
    print(f"Estimated probability that the bulb will have "
        f"a brightness between 1600 and 1700 lumens: {between_1600_and_1700:.4f}")
    print()

if __name__ == "__main__":
    classwork_answers()
    simulation()
