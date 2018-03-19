#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
# This is the script for crawling used car data within 20 miles Madison, from autotrader.
#########################################################################################

import os
import sys
import csv
import json
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
from utility import user_input, write_cars_to_csv


def construct_urls():
    """construct a list of urls for autotrader crawling"""
    maker, model, zipcode, radius, condition = user_input()
    url_list, url_template = [], "https://www.edmunds.com/inventory/srp.html?inventorytype=%s&make=%s&model=%s&radius=%d&zip=%d&pagenumber=%d"
    first_url = url_template%(condition, maker, model, radius, zipcode, 1)
    first_req = Request(first_url, headers={'User-Agent': 'Mozilla/5.0'})
    first_content = urlopen(first_req).read()
    soup = bs(first_content, 'lxml')
    s = soup.find_all('div')[1].find_all('span', class_="small")
    # find total page number
    for i in s:
        m = re.match(r"page 1 of (\d+)", i.getText())
        if m != None:
            break
    total = ((int)(m.groups()[0]))
    for p in range(total):
        url_list.append(url_template%(condition, maker, model, radius, zipcode, p+1))
    return url_list


def main(directory='./'):
    maker, model, zipcode , radius, condition = user_input()
    cars_urls = construct_urls()

    # form output name
    csv_name = "{:s}-{:s}-{:d}-{:d}-{:s}.csv".format(maker, model, zipcode, radius, condition)
    csv_name = os.path.join(directory, csv_name)
    csv_header = ["name", "brand", "vehicleTransmission", "productionDate", "color", "price", "vehicleInteriorColor"]
    # start crawling given a list of autotrader urls
    count = 0
    csv_rows = []
    for url in cars_urls:
        print (url)
        # crawl from a brower setting because of edmunds's anti-crawling'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        oururl = urlopen(req).read()
        soup = bs(oururl, 'lxml')
        # get car info
        cars_info = json.loads(soup.find('script', type='application/ld+json').text)
        # print (cars_info)

        for car in (cars_info[4:]):
            car_info = {"name": car['name'], "brand": car['brand'], "vehicleTransmission":
            car["vehicleTransmission"], "productionDate": car["productionDate"], "color": car["color"],
            "vehicleInteriorColor": car["vehicleInteriorColor"], "price": car["offers"]["price"]}
            # w.writerow(car_info)
            csv_rows.append(dict(car_info))
    write_cars_to_csv(csv_name, csv_header, csv_rows)


if __name__ == "__main__":
  main('../edmunds_data/')
