#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang
##################################
import json
import urllib.request
from bs4 import BeautifulSoup


if __name__ == "__main__":
    url = "https://www.cars.com/for-sale/searchresults.action/?mkId=20049&rd=20&zc=53705&stkTypId=28880&searchSource=QUICK_FORM"
    # url = "https://www.cars.com/for-sale/searchresults.action/?mkId=20028&rd=20&zc=53705&stkTypId=28881&searchSource=QUICK_FORM"
    with urllib.request.urlopen(url) as uopen:
        oururl = uopen.read()
    soup = BeautifulSoup(oururl, 'lxml')
    data = json.loads(soup.find('script', type='application/ld+json').text)
    for car in data:
        print('name = {}; color = {}; price = {}'.format(car['name'], car['color'], car['offers']['price']))
