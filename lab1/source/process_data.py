from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
from pandas import DataFrame
from tabulate import tabulate as table

from data_reader import get_data
from sample_generation import generate_dict


NUMBER_OF_REPEATS: int = 1000


def process_float(number: float) -> str:
    return f"{number:.2f}"


class ProcessDataReturn:
    mean:   float
    median: float
    z_Q:    float

    def to_list(self) -> list[float]:
        return [
            self.mean,
            self.median,
            self.z_Q,
        ]


def process_data(data: np.ndarray) -> ProcessDataReturn:
    result: ProcessDataReturn = ProcessDataReturn()

    result.mean = float(np.mean(data))
    result.median = float(np.median(data))
    result.z_Q = float(np.percentile(data, 25) + np.percentile(data, 75)) / 2

    return result


@dataclass
class ProcessStatReturn:
    E: float
    D: float


def process_stat(data: np.ndarray) -> ProcessStatReturn:
    E = np.mean(data)
    E_2: float = np.mean(data ** 2)
    D = E_2 - E ** 2

    return ProcessStatReturn(E, D)


@dataclass
class ProcessStatsReturn:
    mean:   ProcessStatReturn
    median: ProcessStatReturn
    z_Q:    ProcessStatReturn


def process_stats(func: Callable[[int, ], np.ndarray], size: int) -> ProcessDataReturn:
    data: dict[str, list[int]] = {
        "mean": [],
        "median": [],
        "z_Q": []
    }

    for _ in range(NUMBER_OF_REPEATS):
        sample = func(size)

        processed_data = process_data(sample)
        
        for key, value in data.items():
            value.append(getattr(processed_data, key))
    
    return ProcessStatsReturn(*[process_stat(np.array(value)) for value in data.values()])


def print_data_params(data: dict[str, dict[str, DataFrame]]):
    data_to_print: list[list[Any]] = [["Distribution name", "Size", "E(z)", "E(z^2)", "D(z)", "Med z", "z_Q"], ]
    
    for name, another_data in data.items():
        for size, data in sorted(another_data.items(), key=lambda value: int(value[0])):
            data_to_print.append([name, size, *process_data(data).to_list()])

    print(table(data_to_print, showindex=True))


def print_result(result: dict[str, dict[int, ProcessStatsReturn]]):
    data_to_print: list[list[Any]] = [["Distribution name", "Size", "E(E(z))", "D(E(z))", "E(med z)", "D(med z)", "E(z_Q)", "D(z_Q)"], ]

    for name, another_dict in result.items():
        for size, data in another_dict.items():
            current_data: list[Any] = [name, size, ]

            for stats_param in ["mean", "median", "z_Q"]:
                stat = getattr(data, stats_param)

                for stat_param in ["E", "D"]:
                    current_data.append(process_float(getattr(stat, stat_param)))
            
            data_to_print.append(current_data)
    
    print(table(data_to_print, showindex=True))


def main():
    result: dict[str, dict[int, ProcessStatsReturn]] = {}

    for name, function in generate_dict.items():
        for size in [10, 100, 1000]:
            another_dict: dict[int, ProcessStatsReturn]
            
            if (another_dict := result.get(name)) is None:
                another_dict = {}
                result[name] = another_dict
            
            another_dict[size] = process_stats(function, size)
    
    print_result(result)


if __name__ == "__main__":
    print_data_params(get_data())
