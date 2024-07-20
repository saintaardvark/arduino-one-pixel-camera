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

DEFAULT_DIR = "data"


@click.group()
def show():
    """
    show a file
    """
    pass


def compare_file(filename: str):
    """
    Show comparison for a file
    """
    df = pd.read_csv(filename)
    lib.compare(
        df.T,
    )


def display_file(filename: str, clamp: bool = True):
    """
    Display a file
    """
    df = pd.read_csv(filename)
    if clamp:
        df = lib.clamp_df(df)
    lib.graph(df.T, norm="log")


def write_png(filename: str, png_file: str, clamp: bool = True):
    """
    Read a file, then write it out as a PNG.
    """
    df = pd.read_csv(filename)
    if clamp:
        df = lib.clamp_df(df)
    lib.graph(df.T, norm="log", png_file=png_file)


def find_latest(directory) -> str:
    """
    Find the latest file in directory.

    Args:
      directory (str): directory to search

    Returns:
      str: name of the file with the latest ctime
    """
    list_of_files = glob.glob(f"{directory}/*.csv")
    return max(list_of_files, key=os.path.getctime)


@click.command()
@click.option("--filename")
@click.option("--directory", default=DEFAULT_DIR)
@click.option(
    "--latest/--no-latest",
    default=False,
    help=f"Show latest file in directory (default: {DEFAULT_DIR})",
)
@click.option(
    "--clamp/--no-clamp",
    default=True,
    help=f"Clamp data for better appearance",
)
def display(filename, directory, latest, clamp):
    """
    Display a given filename
    """
    if filename:
        display_file(filename, clamp)
    elif latest:
        display_file(find_latest(directory), clamp)


@click.command()
@click.argument("filename")
@click.option(
    "--clamp/--no-clamp",
    default=True,
    help=f"Clamp data for better appearance",
)
def write(filename, clamp):
    """
    Display a given filename
    """
    png_filename = filename.rstrip(".csv") + ".png"
    print(f"Reading {filename}, writing {png_filename}...")
    write_png(filename, png_filename, clamp)


@click.command()
@click.argument("filename")
@click.option("--directory", default=DEFAULT_DIR)
@click.option(
    "--latest/--no-latest",
    default=False,
    help=f"Show latest file in directory (default: {DEFAULT_DIR})",
)
def compare(filename, directory, latest):
    """
    Show comparisons for given filename
    """
    if filename:
        compare_file(filename)
    elif latest:
        compare_file(find_latest(directory))


show.add_command(display)
show.add_command(compare)
show.add_command(write)


def main():
    """
    Main entry point
    """
    show()


if __name__ == "__main__":
    main()
