#!/usr/bin/env python
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu, Yaqi Zhang
##################################
# This script uses RESTFUl API with JSON-formatted query to fetch car selling data
# from MarketCheck cars and stores the query response into a csv table.
##################################################################################

import numpy as np
import matplotlib.pyplot as plt
import requests
import sys
import csv
import os
import json
from uszipcode import ZipcodeSearchEngine

# Initialize a csv writer for storing web data
def csv_init(output_file, attribute_list):
    csvfile = open(output_file, 'w')
    writer = csv.DictWriter(csvfile, fieldnames=attribute_list)
    writer.writeheader()
    return csvfile, writer

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

def assess_val(dic, key):
    if key not in dic:
        return None
    else:
        return dic[key]

def pipeline(directory='./'):

    maker, model, zipcode , radius, condition = user_input()
    csv_name = "{}-{}-{:d}-{:d}-{:s}.csv".format(maker, model, zipcode, radius, condition)
    csv_name = os.path.join(directory, csv_name)
    if os.path.exists(csv_name):
        try:
            os.remove(csv_name)
            print("delete previous {}".format(csv_name))
        except OSError:
            pass
    f, w = csv_init(csv_name, ["name", "VIN", "year", "price", "miles","Exterior Color", "Interior Color", "seller_name", "seller_phone", "Transmission", "Drivetrain" ])
    # convert zipcode to latitude and longitude
    zipSearch = ZipcodeSearchEngine()
    zipinfo = zipSearch.by_zipcode(str(zipcode))

    latitude, longtitude = str(zipinfo["Latitude"]), str(zipinfo["Longitude"])

    # read assess key for api
    with open("marketcheck_key", "r") as key:
        api_key = key.read()

    car_market_url = "http://api.marketcheck.com/v1/search"

    # start with index = 0, rows = 50 (max cars per request)
    querystring = {"api_key":api_key,"make":maker,"latitude":latitude,"longitude":longtitude,"radius":str(radius),"car_type":condition,"seller_type":"dealer",
    "start":"0", "rows":"50"}

    headers = {'Host': 'marketcheck-prod.apigee.net'}

    response = requests.request("GET", car_market_url, headers=headers, params=querystring)

    cars_json = json.loads(response.text)
    count = (cars_json["num_found"])

    if count % 50:
        num_of_requests = (int)(count/50+1)
    else:
        num_of_requests = (int)(count/50)

    for ite in range(num_of_requests):
        print ("Sending the {:d}th request".format(ite))
        # query the API with new offset json
        if ite !=0:
            querystring["start"] = str(ite*50)
            response = requests.request("GET", car_market_url, headers=headers, params=querystring)
            cars_json = json.loads(response.text)

        for car in cars_json["listings"]:
            car_dict = {"name": assess_val(car,"heading"), "VIN": assess_val(car,"vin"),"price": assess_val(car,"price"), "miles":assess_val(car,"miles"),
            "Exterior Color": assess_val(car,"exterior_color"), "Interior Color": assess_val(car,"interior_color")}
            if assess_val(car,"dealer") != None:
                car_dict["seller_phone"] = assess_val(assess_val(car,"dealer"), "phone")
                car_dict["seller_name"] = assess_val(assess_val(car,"dealer"), "name")
            if assess_val(car,"build") != None:
                car_dict["Transmission"] = assess_val(assess_val(car,"build"), "transmission")
                car_dict["Drivetrain"] = assess_val(assess_val(car,"build"), "drivetrain")
                car_dict["year"] = assess_val(assess_val(car,"build"), "year")
            w.writerow(car_dict)
    f.close()
    print("Writing {:d} cars information to {:s}".format(count, csv_name))
    with open("output.json", "w") as f:
        f.write(response.text)

if __name__ == "__main__":
    pipeline('../market_check_data/')

