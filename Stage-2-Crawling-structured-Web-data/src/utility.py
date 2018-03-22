#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
# This module contains some utility functions
#############################################

import os
import sys
import csv

def user_input():
    """parse command line args"""
    if len(sys.argv) != 8:
        print("Usage: >> python {} <maker> <model> <zip> <radius> <used or new> <json or keyfile> <output_dir>".format(sys.argv[0]))
        print("e.g. python {} Honda Accord 53715 25 used <json or keyfile> ./data/".format(sys.argv[0]))
        sys.exit(1)
    # need to add validation check
    maker = sys.argv[1]
    model = sys.argv[2]
    zipcode = int(sys.argv[3])
    radius = int(sys.argv[4])
    condition = sys.argv[5]
    extra_file = sys.argv[6]
    output_dir = sys.argv[7]
    return (maker, model, zipcode, radius, condition, extra_file, output_dir)

def write_cars_to_csv(csv_name, csv_header, csv_rows):
    """create csv file and write rows to the csv file"""
    # delete previous csv file with the same name
    if os.path.exists(csv_name):
        try:
            os.remove(csv_name)
            print("delete previous {}".format(csv_name))
        except OSError:
            print("error in deleting {}".format(csv_name))
            sys.exit(1)
    with open(csv_name, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=csv_header)
        writer.writeheader()
        for row in csv_rows:
            writer.writerow(row)
    print("Writing {:d} cars information to {:s}".format(len(csv_rows), csv_name))

if __name__ == "__main__":
    print("Hello World")
