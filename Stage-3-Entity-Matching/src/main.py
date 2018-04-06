#!/usr/bin/env python
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu, Yaqi Zhang
##################################

import py_entitymatching as em
import pandas as pd



def merge_by_VIN(table_a="./cars_com_luxury.csv", table_b="./market_check_luxury.csv"):
    table_a_df = pd.read_csv(table_a)
    table_b_df = pd.read_csv(table_b)
    merged_result = pd.merge(table_a_df, table_b_df, how='inner', on="VIN")
    merged_result.to_csv("merged_by_VIN_table.csv", encoding='utf-8',index=False)
    print("Number of tuples resulted by matching table A and table B: ", str(len(merged_result)))

# main method
def main():
    table_a_path = "./cars_com_luxury.csv"
    table_b_path = "./market_check_luxury.csv"

    A = em.read_csv_metadata(table_a_path, key='id')
    B = em.read_csv_metadata(table_b_path, key='id')

    print("Number of tuples in A:{}".format(len(A)))
    print("Number of tuples in B:{}".format(len(B)))

    # let's merge by VIN first
    merge_by_VIN()


if __name__ == "__main__":
  main()

