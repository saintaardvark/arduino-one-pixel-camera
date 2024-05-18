#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.
#
# Licensed under GPL v3.0.  See LICENSE.txt for details.

import sys

import pandas as pd

import lib

def main():
    """
    Main entry point
    """
    print("Here we go!")
    filename = sys.argv[1]
    try:
        df = pd.read_csv(filename)
        lib.graph(df)
    except Exception as e:
        print(f"Error: {e}")
        print("\n\nUsage: show.py [filename]")


if __name__ == "__main__":
    main()
