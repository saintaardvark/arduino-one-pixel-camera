#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.

from datetime import datetime
import serial
import sys


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import numpy as np


DATA = []


def save(data):
    """
    Save data in some way
    """
    # FIXME: Not really CSV
    filename = "data/" + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
    with open(filename, "w") as f:
        f.writelines([f"{i}\n" for i in data])
    print(f"Data file: {filename}")


def munge(data, x=100, reverse=True):
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


# TODO: Look at
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# for live plotting options.
def graph(data):
    """
    Graph data in some way
    """
    print(f"Here's a graph!", data)
    gdata = munge(data, x=1000, reverse=False)
    plt.pcolormesh(gdata, cmap="gray")
    # plt.gca().set_aspect("equal")  # show square as square
    plt.show()
    plt.show()


def log_serial(ser):
    """
    Do the actual logging.

    Assumptions:
    - every line ends with '\r\n'
    - every line is a floating point number

    """
    while True:
        ser_bytes = ser.readline()
        try:
            t = float(ser_bytes.decode("utf-8").rstrip("\r\n"))
            # print(t)
            DATA.append(t)
        except ValueError:
            # not a float? just print it
            print(ser_bytes.decode("utf-8").rstrip("\r\n"))


def main():
    """
    Main entry point
    """
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)
    try:
        log_serial(ser)
    except KeyboardInterrupt:
        save(DATA)
        graph(DATA)
        sys.exit()


if __name__ == "__main__":
    main()
