import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import numpy as np

from .iqd import clamp_df


# TODO: Look at
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# for live plotting options.
def graph(
    data: np.array,
    cmap: str = "gray",
    norm: str = "linear",
    interp: str = "bicubic",
    png_file=None,
):
    """
    Graph data in some way.  Args:

    data: numpy array
    cmap: color map for pcolormesh

    norm: string of name of normalize for pcolormesh;
    Normalize classes not supported.
    """
    plt.imshow(data, cmap=cmap, norm=norm, origin="lower", interpolation=interp)
    if png_file:
        plt.savefig(png_file)
    else:
        plt.show()


def compare(
    df: pd.DataFrame,
    title: str = "New",
    cmap: str = "gray",
    norm: str = "linear",
    interp: str = "bicubic",
):
    """Compare plot of df vs the original"""
    fig, axs = plt.subplots(2, 2)
    fig.suptitle("Comparison")

    axs[0][0].imshow(df, cmap=cmap, norm=norm, origin="lower")
    axs[0][0].set_title("Original")
    axs[0][0].label_outer()

    axs[0][1].imshow(df, cmap=cmap, norm=norm, origin="lower", interpolation=interp)
    axs[0][1].set_title(title)
    axs[0][1].label_outer()

    clamped_df = clamp_df(df)
    axs[1][1].imshow(
        clamped_df, cmap=cmap, norm=norm, origin="lower", interpolation=interp
    )
    axs[1][1].set_title("Clamped")

    flat_df = df.to_numpy().flatten()
    axs[1][0].hist(flat_df, bins=50, edgecolor="black")
    plt.show()


def clamp(df: pd.DataFrame, max: float = 65535.0) -> pd.DataFrame:
    """
    Clamp outlier values to some reasonable amount.
    """


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


def avg_by_col(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate averages of pairs of columns
    Assuming you want to average consecutive pairs
    (column 0 with column 1, column 2 with column 3, etc.)
    """
    num_columns = df.shape[1]
    averaged_df = pd.DataFrame()

    for i in range(0, num_columns, 2):
        if i + 1 < num_columns:
            averaged_column = (df.iloc[:, i] + df.iloc[:, i + 1]) / 2
            averaged_df[f"Averaged_{i}_{i+1}"] = averaged_column
    return averaged_df
