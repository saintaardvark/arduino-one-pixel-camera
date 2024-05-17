import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import numpy as np


# TODO: Look at
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# for live plotting options.
def graph(data: list, x_length: int):
    """
    Graph data in some way
    """
    print(f"Here's a graph!")
    gdata = munge(data, x=x_length, reverse=True)
    plt.pcolormesh(gdata, cmap="gray")
    # plt.gca().set_aspect("equal")  # show square as square
    plt.show()


def othergraph(data: np.array):
    """
    Graph data in some other way
    """
    print(f"Here's a graph!")
    # gdata = munge(data, x=X_LENGTH, reverse=True)
    plt.pcolormesh(data, cmap="gray")
    # plt.gca().set_aspect("equal")  # show square as square
    plt.show()



def munge(data: list, x: int = 100, reverse: bool = True):
    """
    Munge data into 2d array, where x is specified
    and y is int(len(data)/x).

    If reverse is True, then assume every other line
    needs to be reversed -- eg, because we're scanning
    back and forth.
    """
    y = int(len(data) / x)

    n = np.empty((y, x))
    for i in range(int(len(data) / x)):
        start = i * x
        end = (i + 1) * x
        line = data[start:end]
        if i % 2 == 1 and reverse:
            line = list(reversed(line))

        n[i] = line

    return n
