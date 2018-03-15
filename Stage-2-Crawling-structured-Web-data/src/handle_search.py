#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Yaqi Zhang, Jieru Hu
##################################
import re
import json
from pprint import pprint

def main():
    """print id information for different makers and models"""
    data = json.load(open('car_make_model.json'))
    data = data['all']
    for i, maker in enumerate(data, 1):
        print("{:2d}. {:s}\t{:d}".format(i, maker['nm'], maker['id']))
        for j, model in enumerate(maker['md'], 1):
            print("\t{:2d}.{:d} {:s}\t{:d}".format\
                    (i, j, model['nm'], model['id'] if type(model['id']) == int else -1))


def search_makerID_and_modelID(mk, md):
    '''search maker id and model id'''
    data = json.load(open('car_make_model.json'))
    data = data['all']
    for i, maker in enumerate(data, 1):
        if maker['nm'].lower() == mk.lower():
            mkid = maker['id']
            for j, model in enumerate(maker['md'], 1):
                if model['nm'].lower() == md.lower():
                    mdid = model['id']
                    return mkid, mdid
    return None, None


def generate_url(maker, model, zipcode, radius, used=False, page_num=1,num_per_page=100):
    '''generate url according to search'''
    if not used:
        new_used_code = 28880
    else:
        new_used_code = 28881
    template_url = "https://www.cars.com/for-sale/searchresults.action/?mkId=%d&mdId=%d&page=%d&perPage=%d&rd=%d&zc=%d&stkTypId=%d&searchSource=QUICK_FORM"
    mkid, mdid = search_makerID_and_modelID(maker, model)
    if mkid and mdid:
        url = template_url%(mkid, mdid, page_num, num_per_page, int(radius), zipcode, new_used_code)
    return url


def user_input():
    """parse command line args"""
    pass


if __name__ == "__main__":
    # main()
    maker = 'Audi'
    model = 'Q7'
    zipcode = 53705
    radius = 200 # miles
    used = False
    page_num = 1
    num_per_page = 100
    url = generate_url(maker, model, zipcode, radius, used, page_num, num_per_page)
    print(url)
    # url = re.sub(r'page=[0-9]+&perPage=[0-9]+', r'page=%d&perPage=%d', url)
    # print(url)
