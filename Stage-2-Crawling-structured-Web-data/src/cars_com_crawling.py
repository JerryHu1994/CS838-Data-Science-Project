#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
# This is the main file for crawling the web data.

import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import csv
import json

# Initialize a csv writer for storing web data
def csv_init(output_file, attribute_list):
    csvfile = open(output_file, 'w')
    writer = csv.DictWriter(csvfile, fieldnames=attribute_list)
    writer.writeheader()
    return csvfile, writer

# construct a list of urls for cars.com crawling
def construct_urls():
    cars_per_page = 50
    url_list, url_template = [], "https://www.cars.com/for-sale/searchresults.action/?page=%d&perPage=%d&rd=20&searchSource=GN_REFINEMENT&showMore=true&sort=relevance&stkTypId=28881&zc=53715"
    # get number of searched cars
    first_url = url_template%(1, cars_per_page)
    with urllib2.urlopen(first_url) as uopen:
        car_url = uopen.read()
        soup = bs(car_url, 'lxml')
        total_cars = (int)(soup.find_all("div", class_="matchcount")[0].find_all("span", "count")[0].getText().replace(",", ""))
    num_of_urls = total_cars/cars_per_page + 1 if total_cars%cars_per_page else total_cars%cars_per_page
    for i in range((int)(num_of_urls)):
        url_list.append(url_template%(i+1, cars_per_page))
    return url_list

# extract more car infomation from a bs4.element.Tag object into a python dictionary
def get_more_info(car_detail):

    car_miles = car_detail.find('span', class_='listing-row__mileage').text
    car_detail = {"miles": car_miles}
    return car_detail

# main method
def main():
    cars_urls = construct_urls()
    f, w = csv_init("cars_com.csv", ["name", "brand", "color", "price", "seller_name", "seller_phone",
            "seller_average_rating", "seller_review_count"])

    # start crawling given a list of cars.com urls
    for url in cars_urls:
        with urllib2.urlopen(url) as uopen:
            oururl = uopen.read()
        soup = bs(oururl, 'lxml')
        # get car general information from json script
        cars_info = json.loads(soup.find('script', type='application/ld+json').text)

        # get more detailed car information from HTML tags
        cars_detail_list = soup.find_all('div', class_='shop-srp-listings__listing')

        if (len(cars_info) != len(cars_detail_list)):
            print ("Error the size of car json information and size of car html information does not match")
            continue
        # for each car, extract and insert information into csv table
        for ind, car_data in enumerate(cars_info):
            car_info = {"name": car_data['name'], "brand": car_data['brand']['name'], "color":
        car_data['color'], "price": car_data['offers']['price'], "seller_name": car_data['offers']['seller']['name'],
        "seller_phone": car_data['offers']['seller']['telephone'], "seller_average_rating":
        car_data['offers']['seller']['aggregateRating']['ratingValue'], "seller_review_count": car_data['offers']['seller']['aggregateRating']['reviewCount']}
            car_details = get_more_info(cars_detail_list[ind])

            # combine two dicts
            car_dict = {**car_info, **car_details}
            print (car_dict)
            #w.writerow(car_dict)
        f.close()
        return

if __name__ == "__main__":
  main()

