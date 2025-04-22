import matplotlib.pyplot as pyplot
from pandas import DataFrame

from data_reader import get_data


def create_graph(title: str, data: DataFrame, plot_data: list[int, int, int] | None = None):
    axes: pyplot.Axes

    if plot_data is not None:
        plot_data[-1] += 1

        axes = pyplot.subplot(*plot_data)
    else:
        axes = pyplot.subplot()

    pyplot.title(title)

    data.plot.kde(ax=axes)
    data.plot.hist(density=True, ax=axes)

    pyplot.legend().remove()

    pyplot.xlabel('values')

    if plot_data is None:
        pyplot.show()


def create_all(data: dict[str, dict[str, list[float]]]):
    plot_data: list[int, int, int] = [0, 0, 0]

    plot_data[0] = len(data)
    plot_data[1] = max([len(size) for size in data.values()])

    for name, another_data in data.items():
        for size, data in sorted(another_data.items(), key=lambda value: int(value[0])):
            create_graph(f"{name} with size: {size}", data, plot_data)

    pyplot.show()


def main(data: dict[str, dict[str, DataFrame]]):
    pyplot.subplots_adjust(
        left=0.05,
        bottom=0.03,
        right=0.98,
        top=0.97,
        wspace=0.56,
        hspace=0.58,
    )

    create_all(data)


if __name__ == "__main__":
    main(get_data())
