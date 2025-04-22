from typing import Any

import numpy as np
from pandas import DataFrame
from tabulate import tabulate as table

from data_reader import get_data


def process_float(number: float) -> str:
    return f"{number:10.5f}"


class ProcessDataReturn:
    mean:           float
    mean_of_square: float
    median:         float
    variance:       float
    z_Q:            float

    def to_list(self) -> list[str]:
        return [process_float(value) for value in [
            self.mean,
            self.mean_of_square,
            self.variance,
            self.median,
            self.z_Q,
        ]]


def process_data(data: DataFrame) -> ProcessDataReturn:
    result: ProcessDataReturn = ProcessDataReturn()

    mean: float = float(np.mean(data))
    mean_of_square: float = float(np.mean(data ** 2))

    result.mean = mean
    result.mean_of_square = mean_of_square 
    result.median = float(np.median(data))
    result.variance = mean_of_square - mean ** 2
    result.z_Q = float(np.percentile(data, 25) + np.percentile(data, 75)) / 2

    return result


def print_data_params(data: dict[str, dict[str, DataFrame]]):
    data_to_print: list[list[Any]] = [["Distribution name", "Size", "E(z)", "E(z^2)", "D(z)", "Med z", "z_Q"], ]
    
    for name, another_data in data.items():
        for size, data in sorted(another_data.items(), key=lambda value: int(value[0])):
            data_to_print.append([name, size, *process_data(data).to_list()])

    print(table(data_to_print, showindex=True))


def main(data: dict[str, dict[str, DataFrame]]):
    print_data_params(data)


if __name__ == "__main__":
    main(get_data())
