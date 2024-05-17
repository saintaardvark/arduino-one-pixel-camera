#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.
#
# Licensed under GPL v3.0.  See LICENSE.txt for details.

from datetime import datetime
import serial
import sys


import lib

DATA = []
OTHERDATA = np.zeros((90, 90))

BAUDRATE = 115200

X_LENGTH = 1801


def save(data: list, filename: str):
    """
    Save data in some way
    """
    # FIXME: Not really CSV
    df = pd.DataFrame(data)
    with open(filename, "w") as f:
        df.to_csv(f)
    print(f"Data file: {filename}")
    

def munge(data: list, x: int = 100, reverse: bool = True):
    """


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


def log_xy_serial(ser, filename: str):
    count = 0
    while True:
        print("[FIXME] Made it here")
        ser_bytes = ser.readline()
        try:
            # Assumption: format
            # XXXXX [int] YYYYY [int] VAL [int]
            line = ser_bytes.decode("utf-8").rstrip("\r\n")
            if line == "END END END":
                return
            vals = line.split()
            # Assumption: x goes from 0 to 890
            # Assumption: y goes from 90 to 180
            x = int(vals[1])
            # FIXME: off-by-one error in the arduino code, I
            # think...ypos <= END_Y_ANGLE, should prolly be <
            # y = int(vals[3]) - 90 - 1 # zero offset
            y = int(vals[3])
            v = int(vals[5])
            OTHERDATA[x, y] = v
            print(f"OTHERDATA[{x}, {y}] = {v}")
            count += 1
            # Save point: every other line
            if x % 2 == 0 and y % 90 == 0:
                save(OTHERDATA, filename)
        except Exception as e:
            print(f"Couldn't decode that: {e}")
            pass
    


def main():
    """
    Main entry point
    """
    print("Here we go!")
    # ser = serial.Serial("/dev/ttyUSB0", baudrate=BAUDRATE)
    # filename = "data/" + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".csv"
    filename = "data/2024-05-12_14:59:15.csv"
    df = pd.read_csv(filename)
    lib.othergraph(df)


if __name__ == "__main__":
    main()
