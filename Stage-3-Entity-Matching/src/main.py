#!/usr/bin/env python
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu, Yaqi Zhang
##################################

import py_entitymatching as em
import pandas as pd


# main method
def main():
    table_a_path = "../data/cars_com_data/Honda-Accord-53715-25-used.csv"
    table_b_path = "../data/market_check_data/Honda-Accord-53715-25-used.csv"

    A = em.read_csv_metadata(table_a_path, key='VIN')
    B = em.read_csv_metadata(table_b_path, key='VIN')
    print (type(A))

if __name__ == "__main__":
  main()

