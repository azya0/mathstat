from pandas import DataFrame

from create_graph import main as create_graph
from data_reader import get_data
from process_data import main as process_data


def main():
    data: dict[str, dict[str, DataFrame]] = get_data()

    process_data()
    create_graph(data)


if __name__ == "__main__":
    main()
