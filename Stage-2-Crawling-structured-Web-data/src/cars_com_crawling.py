#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
# This is the script for crawling used car data within 20 miles Madison, from cars.com.
import sys
import re
import urllib.request as urllib2
from bs4 import BeautifulSoup as bs
import csv
import json
from handle_search import generate_url
from data_analysis import analyze_price


# Initialize a csv writer for storing web data
def csv_init(output_file, attribute_list):
    csvfile = open(output_file, 'w')
    writer = csv.DictWriter(csvfile, fieldnames=attribute_list)
    writer.writeheader()
    return csvfile, writer

# construct a list of urls for cars.com crawling
def construct_urls():
    cars_per_page = 100
    url_list, url_template = [], "https://www.cars.com/for-sale/searchresults.action/?page=%d&perPage=%d&rd=20&searchSource=GN_REFINEMENT&showMore=true&sort=relevance&stkTypId=28881&zc=53715"
    # get number of searched cars
    first_url = url_template%(1, cars_per_page)
    with urllib2.urlopen(first_url) as uopen:
        car_url = uopen.read()
        soup = bs(car_url, 'lxml')
        total_cars = (int)(soup.find_all("div", class_="matchcount")[0].find_all("span", "count")[0].getText().replace(",", ""))
    num_of_urls = (int)(total_cars/cars_per_page) + 1 if total_cars%cars_per_page else (int)(total_cars/cars_per_page)
    print (num_of_urls)
    for i in range(num_of_urls):
        url_list.append(url_template%(i+1, cars_per_page))
    return url_list


# extract more car infomation from a bs4.element.Tag object into a python dictionary
def get_more_info(car_detail):
    # get mileage
    car_miles = car_detail.find('span', class_='listing-row__mileage')
    if car_miles != None:
        car_miles = (int)(car_miles.text.split()[0].replace(",",""))
    # distance away
    distance = (int)(car_detail.find('div', class_='listing-row__distance listing-row__distance-mobile').text.split()[1])

    car_detail_dict = {"miles": car_miles, "distance_from_Madison" : distance }
    # car meta data
    car_metadata = car_detail.find('ul', class_='listing-row__meta').find_all('li')

    for i in car_metadata:
        [attri, value] = i.text.split(":  ")
        car_detail_dict[attri] = value
    return car_detail_dict


# general version of construct_urls()
def build_urls(start_url):
    cars_per_page = 100
    url_template = re.sub(r'page=[0-9]+&perPage=[0-9]+', r'page=%d&perPage=%d', start_url)
    url_list = []
    # get number of searched cars
    first_url = url_template%(1, cars_per_page)
    with urllib2.urlopen(first_url) as uopen:
        car_url = uopen.read()
        soup = bs(car_url, 'lxml')
        total_cars = (int)(soup.find_all("div", class_="matchcount")[0].find_all("span", "count")[0].getText().replace(",", ""))
    num_of_urls = (int)(total_cars/cars_per_page) + 1 if total_cars%cars_per_page else (int)(total_cars/cars_per_page)
    for i in range(num_of_urls):
        url_list.append(url_template%(i+1, cars_per_page))
    return url_list


# handle command line input return search tuple
def user_input():
    if len(sys.argv) != 6:
        print("Usage: >> python {} <maker> <model> <zip> <radius> <used or new>".\
                format(sys.argv[0]))
        print("e.g. python {} Audi Q7 53705 200 used".format(sys.argv[0]))
        sys.exit(1)
    # need to add validation check
    maker = sys.argv[1]
    model = sys.argv[2]
    zipcode = int(sys.argv[3])
    radius = int(sys.argv[4])
    if sys.argv[5].lower() == "used":
        used = True
    else:
        used = False
    return (maker, model, zipcode, radius, used)


# run the pipeline
def test():
    maker, model, zipcode, radius, used = user_input()
    page_num = 1
    num_per_page = 100
    start_url = generate_url(maker, model, zipcode, radius, used, page_num, num_per_page)
    csv_name = "{}-{}-{:d}-{:d}-{:s}.csv".format(maker, model, zipcode, radius, "used" if used else "new")
    print("crawling...")
    craw_from_url(start_url, csv_name)
    print("finish crawling...")
    analyze_price(csv_name)


# craw from a start url
def craw_from_url(start_url, csv_name):
    url_lst = build_urls(start_url)
    f, w = csv_init(csv_name, ["name", "brand", "color", "price", "seller_name", "seller_phone",
        "seller_average_rating", "seller_review_count", "miles", "distance_from_Madison", "Exterior Color", "Interior Color", "Transmission", "Drivetrain"])
    # start crawling given a list of cars.com urls
    count = 0
    for url in url_lst:
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
            count += 1
            # print (count, ": ", car_data['name'])
            car_info = {"name": car_data['name'], "brand": car_data['brand']['name'], "color":
                    car_data['color'], "price": car_data['offers']['price'], "seller_name": car_data['offers']['seller']['name']}
            # need to check for telephone because some sellers does not have telephone
            if 'telephone' in car_data['offers']['seller']:
                car_info['seller_phone'] = car_data['offers']['seller']['telephone']

            # need to check for aggregateRating because some seller does not have rating
            if 'aggregateRating' in car_data['offers']['seller']:
                car_info['seller_average_rating'] = car_data['offers']['seller']['aggregateRating']['ratingValue']
                car_info['seller_review_count'] = car_data['offers']['seller']['aggregateRating']['reviewCount']

            car_details = get_more_info(cars_detail_list[ind])

            # combine two dicts
            car_dict = {**car_info, **car_details}

            # write current dict to csv file
            w.writerow(car_dict)
    f.close()
    print("Writing {:d} cars information to {:s}".format(count, csv_name))


# main method
def main():
    cars_urls = construct_urls()
    f, w = csv_init("cars_com.csv", ["name", "brand", "color", "price", "seller_name", "seller_phone",
            "seller_average_rating", "seller_review_count", "miles", "distance_from_Madison", "Exterior Color", "Interior Color", "Transmission", "Drivetrain"])
    # start crawling given a list of cars.com urls
    count = 0
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
            count += 1
            print (count, ": ", car_data['name'])
            car_info = {"name": car_data['name'], "brand": car_data['brand']['name'], "color":
        car_data['color'], "price": car_data['offers']['price'], "seller_name": car_data['offers']['seller']['name']}
            # need to check for telephone because some sellers does not have telephone
            if 'telephone' in car_data['offers']['seller']:
                car_info['seller_phone'] = car_data['offers']['seller']['telephone']

            # need to check for aggregateRating because some seller does not have rating
            if 'aggregateRating' in car_data['offers']['seller']:
                car_info['seller_average_rating'] = car_data['offers']['seller']['aggregateRating']['ratingValue']
                car_info['seller_review_count'] = car_data['offers']['seller']['aggregateRating']['reviewCount']

            car_details = get_more_info(cars_detail_list[ind])

            # combine two dicts
            car_dict = {**car_info, **car_details}
            #print (car_dict)
            # write current dict to csv file
            w.writerow(car_dict)
    f.close()

if __name__ == "__main__":
  # main()
  test()
