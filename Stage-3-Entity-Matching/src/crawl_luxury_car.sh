#!/bin/sh
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu, Yaqi Zhang
##################################
# bash script that do the crawling
##################################

cd ../../Stage-2-Crawling-structured-Web-data/src/

# crawl from cars.com
# python cars_com_crawling.py mb all 53715 75 all cars_com_make_model.json ../data/cars_com_data/
# python cars_com_crawling.py bmw all 53715 75 all cars_com_make_model.json ../data/cars_com_data/
# python cars_com_crawling.py audi all 53715 75 all cars_com_make_model.json ../data/cars_com_data/
# python cars_com_crawling.py lexus all 53715 75 all cars_com_make_model.json ../data/cars_com_data/

# crawl from marketcheck
# python ./marketcheck_car_api.py BMW all 53715 90 used marketcheck_key ../data/market_check_data/
# python ./marketcheck_car_api.py Mercedes-Benz all 53715 90 used marketcheck_key ../data/market_check_data/
# python ./marketcheck_car_api.py Audi all 53715 90 used marketcheck_key ../data/market_check_data/
# python ./marketcheck_car_api.py Lexus all 53715 90 used marketcheck_key ../data/market_check_data/

cd ../../Stage-3-Entity-Matching/src/

# merge csv
python merge_csv.py cars_com_luxury.csv ../../Stage-2-Crawling-structured-Web-data/data/cars_com_data/
python merge_csv.py market_check_luxury.csv ../../Stage-2-Crawling-structured-Web-data/data/market_check_data/

wc -l cars_com_luxury.csv
wc -l market_check_luxury.csv


