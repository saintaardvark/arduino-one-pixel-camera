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

import lib


DATA = []
OTHERDATA = np.zeros((45, 45))

BAUDRATE = 115200

X_LENGTH = 1801


def save(data: np.array, filename: str):
    """
    Save data to a file.  Currently, converts to a Pandas
    dataframe then saves as CSV.

    Args:
      data (np.array): data to save
      filename (str): filename
    """
    # FIXME: Not really CSV
    df = pd.DataFrame(data)
    with open(filename, "w") as f:
        df.to_csv(f, index_label=False)


# TODO: annotation for the ser variable
def log_serial(ser: serial.Serial) -> int:
    """
    Do the actual logging.

    Assumptions:
    - every line ends with '\r\n'
    - every line is a floating point number

    Args:
      ser (serial.Serial): the serial port to open

    returns:
        x_length (int): length of each line (eg, number of samples on
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


def log_xy_serial(ser: serial.Serial, filename: str) -> np.array:
    """
    Log the xy data by putting it in a numpy array.  Save
    it to a file every so often by saving it to a file.

    Args:
      ser (serial.Serial): serial port
      filename (str): Filename to save to

    Returns:
      np.array: the data read from the camera
    """
    count = 0
    # The first line should be the size of the array
    ser_bytes = ser.readline()
    # Assumption: format
    # MAX_X [int] MAX_Y [int]
    line = ser_bytes.decode("utf-8").rstrip("\r\n")
    vals = line.split()
    print(vals)
    x = int(vals[1])
    y = int(vals[3])
    print(f"{x=} {y=}")
    data = np.zeros((x, y))
    while True:
        ser_bytes = ser.readline()
        try:
            # Assumption: format
            # XXXXX [int] YYYYY [int] VAL [int]
            line = ser_bytes.decode("utf-8").rstrip("\r\n")
            if line == "END END END":
                return data
            vals = line.split()
            x = int(vals[1])
            y = int(vals[3])
            v = int(vals[5])
            data[x, y] = v
            print(f"data[{x}, {y}] = {v}")
            count += 1
            # Save point: every other line
            if x % 2 == 0 and y == 0:
                save(data, filename)
        except Exception as e:
            print(f"Couldn't decode that: {e}")
            pass


def main():
    """
    Main entry point
    """
    print("Here we go!")
    ser = serial.Serial("/dev/ttyUSB0", baudrate=BAUDRATE)
    filename = "data/" + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
    x_length = 0
    try:
        # The firmware waits for input before continuing
        ser.write(bytes("\n", "utf-8"))
        start = datetime.now()
        data = log_xy_serial(ser, filename)
        end = datetime.now()
        print(f"That took {(end - start).seconds} seconds")
        save(data, filename)
    except KeyboardInterrupt:
        save(data, filename)
    print(f"Data file: {filename}")
    lib.compare(pd.DataFrame(data).T)


if __name__ == "__main__":
    main()
