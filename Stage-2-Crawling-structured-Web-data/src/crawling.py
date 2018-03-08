#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu
##################################
# This is the main file for crawling the web data.

import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt
import csv

# Initialize a csv writer for storing web data
def csv_init(output_file, attribute_list):
    csvfile = open(output_file, 'w')
    writer = csv.DictWriter(csvfile, fieldnames=attribute_list)
    writer.writeheader()
    return csvfile, writer

# main method
def main():
    page = urllib2.urlopen("https://www.cars.com/vehicledetail/detail/715765573/overview/")
    soup = bs(page,"html.parser")
    #f, w = csv_init("out.csv", ['first', 'second'])
    #w.writerow({'first':'fff', 'second':'sss'})
    print (soup.title)
    print (soup.find_all('a'))
    #f.close()

if __name__ == "__main__":
  main()

