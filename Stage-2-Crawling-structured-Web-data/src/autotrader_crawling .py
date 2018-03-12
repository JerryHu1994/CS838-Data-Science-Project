#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
# This is the script for crawling used car data within 20 miles Madison, from autotrader.

import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import csv
import json
import re

# Initialize a csv writer for storing web data
def csv_init(output_file, attribute_list):
    csvfile = open(output_file, 'w')
    writer = csv.DictWriter(csvfile, fieldnames=attribute_list)
    writer.writeheader()
    return csvfile, writer

# construct a list of urls for autotrader crawling
def construct_urls():
    url_list, url_template = [], ""
    return url_list

# main method
def main():
    cars_urls = construct_urls()
    f, w = csv_init("autotrader.csv", [])
    # start crawling given a list of autotrader urls
    count = 0
    for url in cars_urls:
        with urllib2.urlopen(url) as uopen:

    f.close()

if __name__ == "__main__":
  main()

