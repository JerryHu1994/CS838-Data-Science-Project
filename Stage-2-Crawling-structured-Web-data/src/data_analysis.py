#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
"""
This module contains some functions
that analyzes car data in csv file
"""
# standard library
import os
import sys

# third party library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def add_year_column(df):
    """
    extract year info from name column and create a new column called year

    Args:
        df: Data Frame crawled from cars.com

    Returns:
        new Data Frame with year column added
    """
    names = df['name']
    years = []
    for name in names:
        year_str = name.split()[0]
        try:
            year = int(year_str)
        except ValueError:
            year = 2018  # 0
        years.append(year)
    df['year'] = years


def extract_cars(df, requirement):
    """
    filter all the cars satisfy the requirement

    Args:
        df: Data Frame crawled from cars.com
        requirement: e.g. ('price', (50000, 60000))
                          ('distance', (0, 100))

    Returns:
        all the data satisfying the requirement
    """
    attribute = requirement[0]
    if attribute == 'price':
        low, high = requirement[1]
    elif attribute == 'distance':
        for item in df.columns:
            if item.startswith('distance_from'):
                attribute = item
                break
        low, high = requirement[1]
    else:
        print("unsupport attribute {}".format(attribute))
        sys.exit(1)
    new_df = df[(df[attribute] >= low) & (df[attribute] <= high)]
    return new_df


def print_df(df):
    """
    only print the most important info (name, price, color) of cars,
    and sort by price

    Args:
        df: Data Frame crawled from cars.com

    Returns:
        None
    """
    if df.empty:
        print("Data frame is empty!")
    else:
        print(df[['name', 'price', 'color']].sort_values('price'))


def load_csvfile(csvfile):
    """
    check existence and load csv file to pandas data frame

    Args:
        csvfile: csv filename

    Returns:
        Data Frame loaded from csv file
    """
    if not os.path.exists(csvfile):
        print("{} does not exist".format(csvfile))
        sys.exit(1)
    df = pd.read_csv(csvfile)
    return df


def analyze_price(df, maker, model, plot=False):
    """
    analyze car price and give a rough idea how expensive the car is

    Args:
        df: Data Frame crawled from cars.com
        plot: whether plot the histgram or not

    Returns:
        price_info: a dictionary
    """
    if plot:
        df = df[np.isfinite(df['price'])]
        plt.hist(df['price'].values)
        plt.xlabel('price')
        plt.ylabel('number')
    price_info = df['price'].describe()
    print("Some Price Information ({}-{}):".format(maker, model))
    n = len('median price')
    print("{:s} = $ {:,.2f}".format('min price'.ljust(n), price_info['min']))
    print("{:s} = $ {:,.2f}".format('mean price'.ljust(n), price_info['mean']))
    print(
        "{:s} = $ {:,.2f}".format(
            'median price'.ljust(n),
            df['price'].median()))
    print("{:s} = $ {:,.2f}".format('max price'.ljust(n), price_info['max']))
    print("{:s} = $ {:,.2f}".format('std price'.ljust(n), price_info['std']))


def main():
    """show how to use analyze_price()"""
    if len(sys.argv) != 2:
        print("Usage: >> python {} <csvfile>".format(sys.argv[0]))
        sys.exit(1)
    csvfile = sys.argv[1]
    df = load_csvfile(csvfile)
    if '/' in csvfile:
        csvfile = csvfile[csvfile.rfind('/') + 1:]
    maker, model = csvfile.split('-')[:2]
    maker = maker.upper()
    model = model.upper()
    analyze_price(df, maker, model, plot=False)
    new_df = extract_cars(df, ('price', (90000, 110000)))
    print_df(new_df)
    add_year_column(df)
    plt.show()


if __name__ == "__main__":
    main()
