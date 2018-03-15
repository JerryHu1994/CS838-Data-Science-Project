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

def analyze_price(csvfile):
    """analyze car price and give a rough idea how expensive the car is"""
    if not os.path.exists(csvfile):
        print("{} does not exist".format(csvfile))
        sys.exit(1)
    df = pd.read_csv(csvfile)
    df = df[np.isfinite(df['price'])]
    # plt.subplot(111)
    plt.hist(df['price'].values)
    plt.xlabel('price')
    plt.ylabel('number')
    price_info = df['price'].describe()
    maker, model = csvfile.split('-')[:2]
    maker = maker.upper()
    model = model.upper()
    print("Some Price Information ({}-{}):".format(maker, model))
    n = len('median price')
    print("{:s} = $ {:0.2f}".format('min price'.ljust(n), price_info['min']))
    print("{:s} = $ {:0.2f}".format('mean price'.ljust(n), price_info['mean']))
    print("{:s} = $ {:0.2f}".format('median price'.ljust(n), df['price'].median()))
    print("{:s} = $ {:0.2f}".format('max price'.ljust(n), price_info['max']))


def main():
    """show how to use analyze_price()"""
    if len(sys.argv) != 2:
        print("Usage: >> python {} <csvfile>".format(sys.argv[0]))
        sys.exit(1)
    csvfile = sys.argv[1]
    analyze_price(csvfile)
    plt.show()

if __name__ == "__main__":
    main()

