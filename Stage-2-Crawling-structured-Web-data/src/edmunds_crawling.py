#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
# This is the script for crawling used car data within 20 miles Madison, from autotrader.

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import csv
import json
import re
import sys
import os

# Initialize a csv writer for storing web data
def csv_init(output_file, attribute_list):
    csvfile = open(output_file, 'w')
    writer = csv.DictWriter(csvfile, fieldnames=attribute_list)
    writer.writeheader()
    return csvfile, writer

# handle command line input return search tuple
def user_input():
    if len(sys.argv) != 6:
        print("Usage: >> python {} <maker> <model> <zip> <radius> <used or new>".\
                format(sys.argv[0]))
        print("e.g. python {} Honda Accord 53715 25 used".format(sys.argv[0]))
        sys.exit(1)
    # need to add validation check
    maker = sys.argv[1]
    model = sys.argv[2]
    zipcode = int(sys.argv[3])
    radius = int(sys.argv[4])
    condition = sys.argv[5]
    return (maker, model, zipcode, radius, condition)


# construct a list of urls for autotrader crawling
def construct_urls():
    maker, model, zipcode, radius, condition = user_input()
    url_list, url_template = [], "https://www.edmunds.com/inventory/srp.html?inventorytype=%s&make=%s&model=%s&radius=%d&zip=%d&pagenumber=%d"
    url = url_template%(condition, maker, model, radius, zipcode, 1)
    #return url_list
    return [url]

# main method
def main(directory='./'):
    maker, model, zipcode , radius, condition = user_input()
    cars_urls = construct_urls()

    # form output name
    csv_name = "{:s}-{:s}-{:d}-{:d}-{:s}.csv".format(maker, model, zipcode, radius, condition)
    csv_name = os.path.join(directory, csv_name)
    f, w = csv_init(csv_name, ["name", "brand", "vehicleTransmission", "productionDate", "color", "price", "vehicleInteriorColor"])
    # start crawling given a list of autotrader urls
    count = 0
    for url in cars_urls:
        # crawl from a brower setting because of edmunds's anti-crawling'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        oururl = urlopen(req).read()
        soup = bs(oururl, 'lxml')
        # get car info
        cars_info = json.loads(soup.find('script', type='application/ld+json').text)

        for car in (cars_info[4:]):
            car_info = {"name": car['name'], "brand": car['brand'], "vehicleTransmission":
            car["vehicleTransmission"], "productionDate": car["productionDate"], "color": car["color"],
            "vehicleInteriorColor": car["vehicleInteriorColor"], "price": car["offers"]["price"]}
            print (car_info)
            w.writerow(car_info)
    f.close()

if __name__ == "__main__":
  main('../edmunds_data/')

