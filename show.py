#!/usr/bin/env python3

# Simple serial logger.  Lots of assumptions.
#
# Licensed under GPL v3.0.  See LICENSE.txt for details.

import glob
import os
import sys

import click
import pandas as pd

import lib


@click.group()
def show():
    """
    show a file
    """
    pass


def display(filename: str):
    """
    display
    """
    df = pd.read_csv(filename)
    lib.compare(df.T)


@click.command()
@click.option("--directory", default="data")
def latest(directory):
    # Ensure the directory path ends with a slash
    list_of_files = glob.glob(f"{directory}/*.csv")
    latest_file = max(list_of_files, key=os.path.getctime)
    display(latest_file)


@click.command()
@click.option("--filename")
def file(filename):
    display(filename)

show.add_command(latest)
show.add_command(file)

def main():
    """
    Main entry point
    """
    show()


if __name__ == "__main__":
    main()
