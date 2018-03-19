#!/usr/bin/env python
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu, Yaqi Zhang
##################################
# This script uses RESTFUl API with JSON-formatted query to fetch car selling data
# from MarketCheck cars and stores the query response into a csv table.
##################################################################################

import os
import json
import requests
from uszipcode import ZipcodeSearchEngine
from utility import user_input, write_cars_to_csv


def pipeline_market_check(directory='./'):
    """the whole crawling pipeline"""
    maker, model, zipcode, radius, condition = user_input()

    # convert zipcode to latitude and longitude
    zipSearch = ZipcodeSearchEngine()
    zipinfo = zipSearch.by_zipcode(str(zipcode))
    latitude, longtitude = str(zipinfo["Latitude"]), str(zipinfo["Longitude"])

    # read assess key for api
    with open("marketcheck_key", "r") as key:
        api_key = key.read()

    car_market_url = "http://api.marketcheck.com/v1/search"

    # start with index = 0, rows = 50 (max cars per request)
    max_rows_per_request = 50
    querystring = {"api_key" : api_key,
            "make" : maker,
            "model" : model,
            "latitude" : latitude,
            "longitude" : longtitude,
            "radius" : str(radius),
            "car_type" : condition,
            "seller_type" : "dealer",
            "start" : "0",
            "rows" : str(max_rows_per_request),
            }

    headers = {'Host': 'marketcheck-prod.apigee.net'}

    response = requests.request("GET", car_market_url, headers=headers,\
            params=querystring)

    cars_json = json.loads(response.text)
    count = (cars_json["num_found"])
    num_of_requests = (count + max_rows_per_request - 1) // max_rows_per_request
    print("Total number of request is {:d}".format(num_of_requests))

    short_csv_header = ["Name", "VIN", "Price", "Miles", "Exterior Color", "Interior Color"]
    dict_header = ["heading", "vin", "price", "miles", "exterior_color", "interior_color"]
    long_csv_header = ["Name", "VIN", "Year", "Price", "Miles",\
            "Exterior Color", "Interior Color", "Seller Name", \
            "Seller Phone", "Transmission", "Drivetrain" ]
    csv_rows = [] # store crawled data

    for ite in range(num_of_requests):
        print ("Sending the {:d}th request".format(ite))
        # query the API with new offset json
        if ite !=0:
            querystring["start"] = str(ite * max_rows_per_request)
            response = requests.request("GET", car_market_url,\
                    headers=headers, params=querystring)
            cars_json = json.loads(response.text)

        for car in cars_json["listings"]: # car is a dictionary
            car_dict = {ch : car.get(dh, None)
                    for ch, dh in zip(short_csv_header, dict_header)}
            if "dealer" in car:
                dealer = car["dealer"]
                car_dict["Seller Phone"] = dealer.get("phone", None)
                car_dict["Seller Name"] = dealer.get("name", None)
            if "build" in car:
                build = car["build"]
                car_dict["Transmission"] = build.get("transmission", None)
                car_dict["Drivetrain"] = build.get("drivetrain", None)
                car_dict["Year"] = build.get("year", None)
            csv_rows.append(dict(car_dict))

    # write data to csv file
    csv_name = "{}-{}-{:d}-{:d}-{:s}.csv".format(maker, model, zipcode, \
            radius, condition)
    csv_name = os.path.join(directory, csv_name)
    write_cars_to_csv(csv_name, long_csv_header, csv_rows)
    # why this?
    # with open("output.json", "w") as f:
    #    f.write(response.text)


if __name__ == "__main__":
    pipeline_market_check('../market_check_data/')
