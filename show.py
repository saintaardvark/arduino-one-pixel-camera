#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.
#
# Licensed under GPL v3.0.  See LICENSE.txt for details.

import pandas as pd

import lib

def main():
    """
    Main entry point
    """
    print("Here we go!")
    filename = "data/2024-05-12_14:59:15.csv"
    df = pd.read_csv(filename)
    lib.othergraph(df)


if __name__ == "__main__":
    main()
