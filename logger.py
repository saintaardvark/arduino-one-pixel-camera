#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.
#
# Licensed under GPL v3.0.  See LICENSE.txt for details.

from datetime import datetime
import serial
import sys


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import numpy as np


DATA = []
OTHERDATA = np.zeros((90, 90))

X_LENGTH = 1801


def save(data: list):
    """
    Save data in some way
    """
    # FIXME: Not really CSV
    df = pd.DataFrame(data)
    filename = "data/" + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
    with open(filename, "w") as f:
        df.to_csv(f)
    print(f"Data file: {filename}")
    

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


# TODO: Look at
# https://stackoverflow.com/questions/28269157/plotting-in-a-non-blocking-way-with-matplotlib
# for live plotting options.
def graph(data: list, x_length: int = X_LENGTH):
    """
    Graph data in some way
    """
    print(f"Here's a graph!")
    gdata = munge(data, x=X_LENGTH, reverse=True)
    plt.pcolormesh(gdata, cmap="gray")
    # plt.gca().set_aspect("equal")  # show square as square
    plt.show()


def othergraph(data: np.array = OTHERDATA):
    """
    Graph data in some other way
    """
    print(f"Here's a graph!")
    # gdata = munge(data, x=X_LENGTH, reverse=True)
    plt.pcolormesh(data, cmap="gray")
    # plt.gca().set_aspect("equal")  # show square as square
    plt.show()


# TODO: annotation for the ser variable
def log_serial(ser):
    """
    Do the actual logging.

    Assumptions:
    - every line ends with '\r\n'
    - every line is a floating point number

    returns: x_length, length of each line (eg, number of samples on
    a single scan line)
    """
    last = 0
    x_length = 0
    while True:
        ser_bytes = ser.readline()
        try:
            t = float(ser_bytes.decode("utf-8").rstrip("\r\n"))
            # print(t)
            DATA.append(t)
        except ValueError:
            # not a float? just print it, plus how many samples we have now
            try:
                print(ser_bytes.decode("utf-8").rstrip("\r\n"))
                new_samples = len(DATA) - last
                print(new_samples)
                last = len(DATA)
                if x_length < last:
                    x_length = last
            except Exception as e:
                print(f"Couldn't decode that: {e}")
                pass
    return x_length


def log_xy_serial(ser):
    x_length = 9999 # FIXME
    while True:
        ser_bytes = ser.readline()
        try:
            # Assumption: format
            # XXXXX [int] YYYYY [int] VAL [int]
            line = ser_bytes.decode("utf-8").rstrip("\r\n")
            vals = line.split()
            # Assumption: x goes from 0 to 890
            # Assumption: y goes from 90 to 180
            x = int(vals[1])
            # FIXME: off-by-one error in the arduino code, I
            # think...ypos <= END_Y_ANGLE, should prolly be <
            y = int(vals[3]) - 90 - 1 # zero offset
            v = int(vals[5])
            OTHERDATA[x, y] = v
            print(f"OTHERDATA[{x}, {y}] = {v}")
        except Exception as e:
            print(f"Couldn't decode that: {e}")
            pass
    return x_length
    


def main():
    """
    Main entry point
    """
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)
    x_length = 0
    try:
        # x_length = log_serial(ser)
        xy_data = log_xy_serial(ser)
    except KeyboardInterrupt:
        save(OTHERDATA)
        othergraph(OTHERDATA)
        sys.exit()


if __name__ == "__main__":
    main()
