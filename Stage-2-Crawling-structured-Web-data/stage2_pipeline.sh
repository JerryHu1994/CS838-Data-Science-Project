#!/bin/bash
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu, Yaqi Zhang
##################################
# Stage 2 pipeline example
##################################

make="Honda"
model="Accord"
zipcode=53715
radius=25
condition="used"
car_json_file="./src/cars_com_make_model.json"
marketcheck_key="./src/marketcheck_key"
cars_outdir="./data/cars_com_data/"
market_outdir="./data/market_check_data/"
echo "Crawling $condition $make-$model from cars.com, in $zipcode with $radius miles"
python ./src/cars_com_crawling.py $make $model $zipcode $radius $condition $car_json_file $cars_outdir

echo "Crawling $condition $make-$model from marketcheck, in $zipcode with $radius miles"
python ./src/marketcheck_car_api.py $make $model $zipcode $radius $condition $marketcheck_key $market_outdir
