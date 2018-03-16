#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_cars(df, requirement):
    """filter all the cars satisfy the requirement
       requirement: ('price', (50000, 60000))
                    ('distance', (0, 100))
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
    """only print the most important info of cars"""
    print(df[['name', 'price', 'color']].sort_values('price'))

def load_csvfile(csvfile):
    """load csv file to pandas data frame"""
    if not os.path.exists(csvfile):
        print("{} does not exist".format(csvfile))
        sys.exit(1)
    df = pd.read_csv(csvfile)
    return df

def analyze_price(df, maker, model, plot=False):
    """analyze car price and give a rough idea how expensive the car is"""
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
    print("{:s} = $ {:,.2f}".format('median price'.ljust(n), df['price'].median()))
    print("{:s} = $ {:,.2f}".format('max price'.ljust(n), price_info['max']))
    print("{:s} = $ {:,.2f}".format('std price'.ljust(n), price_info['std']))

def main():
    """show how to use analyze_price()"""
    if len(sys.argv) != 2:
        print("Usage: >> python {} <csvfile>".format(sys.argv[0]))
        sys.exit(1)
    csvfile = sys.argv[1]
    df = load_csvfile(csvfile)
    maker, model = csvfile.split('-')[:2]
    maker = maker.upper()
    model = model.upper()
    analyze_price(df, maker, model, plot=False)
    new_df = extract_cars(df, ('price', (90000, 110000)))
    print_df(new_df)
    plt.show()

if __name__ == "__main__":
    main()
