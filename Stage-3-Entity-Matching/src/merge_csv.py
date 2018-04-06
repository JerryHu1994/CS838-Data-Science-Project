#!/usr/bin/env python
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu
##################################
# This file takes into a list of csv files and merge them into a single csv file.
import numpy as np
import pandas as pd
import os
import sys

# main method
def main():
    if len(sys.argv) != 3:
        print ("Usage: >> python {} outfile csv_folder".format(sys.argv[0]))
        sys.exit(1)
    csv_path = sys.argv[2]
    if not os.path.exists(csv_path):
        print ("{} not found".format(csv_path))
    csv_files = [csv_path+f for f in os.listdir(csv_path)]
    all_data = [pd.read_csv(f) for f in csv_files]
    merged_data = pd.concat(all_data, ignore_index=True)
    merged_data['id'] = range(0, len(merged_data))
    merged_data.to_csv(sys.argv[1], encoding='utf-8',index=False)

if __name__ == "__main__":
  main()

