import os

from pandas import DataFrame

from config import PATH


def get_data_from_file(filename: str) -> list[int]:
    try:
        with open(f"{PATH}/{filename}") as file:
            return DataFrame(list(
                map(float, file.readline().strip().split(", ")))
            )
    except ValueError as error:
        print(f"Value error in {filename}: {error}")


def get_data() -> dict[str, dict[str, DataFrame]]:
    result: dict[str, dict[str, DataFrame]] = {}
    
    for filename in os.listdir(PATH):
        name, _, size = filename.split(".")[0].split("_")

        data = get_data_from_file(filename)

        if result.get(name) is None:
            result[name] = {}
        
        result[name][size] = data
    
    return result
