#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu, Yaqi Zhang
##################################
# This file takes into a list of 
# csv files and merge them into a 
# single csv file.
##################################

import os
import sys
import numpy as np
import pandas as pd

# main method
def main():
    if len(sys.argv) != 3:
        print ("Usage: >> python {} outfile csv_folder".format(sys.argv[0]))
        sys.exit(1)
    csv_path = sys.argv[2]
    if not os.path.exists(csv_path):
        print ("{} not found".format(csv_path))
        sys.exit(1)
    # csv_files = [csv_path+f for f in os.listdir(csv_path)]
    csv_files = [os.path.join(csv_path, f) for f in os.listdir(csv_path) if f.endswith('.csv')]
    all_data = [pd.read_csv(f) for f in csv_files]
    merged_data = pd.concat(all_data, ignore_index=True)
    merged_data.to_csv(sys.argv[1], encoding='utf-8',index=False)

if __name__ == "__main__":
    main()

