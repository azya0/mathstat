import os
from typing import Callable

import numpy as np

from config import PATH


def generate_normal_samples(size: int):
    return np.random.normal(loc=0, scale=1, size=size)


def generate_cauchy_samples(size: int):
    return np.random.standard_cauchy(size=size)


def generate_poisson_samples(size: int):
    return np.random.poisson(lam=10, size=size)


def generate_uniform_samples(size: int):
    lower_bound = -np.sqrt(3)
    upper_bound = np.sqrt(3)
    return np.random.uniform(low=lower_bound, high=upper_bound, size=size)


generate_dict: dict[str, Callable[[int], np.ndarray]] = {
    "normal_distribution": generate_normal_samples,
    "Cauchy_distribution": generate_cauchy_samples,
    "Poisson_distribution": generate_poisson_samples,
    "uniform_distribution": generate_uniform_samples
}


def create_all_distribution(size: int):
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    
    for name, function in generate_dict.items():
        with open(f"{PATH}/{name}_{size}.txt", "w") as file:
            for index, number in enumerate(function(size)):
                if index != 0:
                    file.write(", ")
                
                file.write(str(number))


if __name__ == "__main__":
    for size in [10, 50, 1000, 10000]:
        create_all_distribution(size)
