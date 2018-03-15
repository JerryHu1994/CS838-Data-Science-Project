#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_price(csvfile):
    df = pd.read_csv(csvfile)
    df = df[np.isfinite(df['price'])]
    # plt.subplot(111)
    plt.hist(df['price'].values)
    plt.xlabel('price')
    plt.ylabel('number')
    price_info = df['price'].describe()
    print("min price = ${:0.2f}".format(price_info['min']))
    print("mean price = ${:0.2f}".format(price_info['mean']))
    print("max price = ${:0.2f}".format(price_info['max']))


def main():
    if len(sys.argv) != 2:
        print("Usage: >> python {} <csvfile>".format(sys.argv[0]))
        sys.exit(1)
    csvfile = sys.argv[1]
    analyze_price(csvfile)
    plt.show()

if __name__ == "__main__":
    main()

