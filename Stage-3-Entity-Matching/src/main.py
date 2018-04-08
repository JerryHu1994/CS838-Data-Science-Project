#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu, Yaqi Zhang
##################################
# main program
##################################
import py_entitymatching as em
import pandas as pd
import math

def merge_by_VIN(table_a="./cars_com_luxury.csv", table_b="./market_check_luxury.csv"):
    table_a_df = pd.read_csv(table_a)
    table_b_df = pd.read_csv(table_b)
    merged_result = pd.merge(table_a_df, table_b_df, how='inner', on="VIN")
    merged_result.to_csv("merged_by_VIN_table.csv", encoding='utf-8',index=False)
    print("Number of tuples resulted by matching table cars_com and table market_check: ", str(len(merged_result)))

# Match car_a and car_b when the year differs no more than one
def compare_car_year(car_a, car_b):
    if math.isnan(car_b['year']):
        return True
    if abs((int)(car_a['year']) - (int)(car_b['year'])) <= 1:
        return True
    else:
        return False

# main method
def main():
    cars_com_path = "./cars_com_luxury.csv"
    market_check_path = "./market_check_luxury.csv"

    cars_com_data = em.read_csv_metadata(cars_com_path, key='id')
    market_check_data = em.read_csv_metadata(market_check_path, key='id')

    print("Number of tuples in cars_com:{}".format(len(cars_com_data)))
    print("Number of tuples in market_check:{}".format(len(market_check_data)))

    # let's merge by VIN first
    # merge_by_VIN()

    # downsampling
    print("Downsampling the input data...")
    cars_com_downsampled, market_check_downsampled = em.down_sample(cars_com_data, market_check_data,
    size=1000, y_param=1, show_progress=False)
    print("Number of tuples in cars_com after downsampling: {}".format(len(cars_com_downsampled)))
    print("Number of tutple in market_check after downsampling: {}".format(len(market_check_downsampled)))

    # blocking stage
    brand_block = em.OverlapBlocker()
    l_attri_kept = ["name", "price", "seller_name", "miles", "distance_from_Madison"]
    r_attri_kept = ["name", "price", "Seller Name", "miles", ]
    # 1st block on brand
    brand_block_result = brand_block.block_tables(cars_com_downsampled, market_check_downsampled, 'brand','make', word_level=True,
    overlap_size=1, l_output_attrs=l_attri_kept, r_output_attrs=r_attri_kept, show_progress=False)

    block_f = em.get_features_for_blocking(cars_com_downsampled, market_check_downsampled)
    block_f
    # 2nd block on year
    year_block = em.RuleBasedBlocker()
    year_block.add_rule(['year_year_lev_sim(ltuple, rtuple) < 0.8'], block_f)
    year_block_result = year_block.block_tables(cars_com_downsampled, market_check_downsampled,
    l_output_attrs=l_attri_kept, r_output_attrs=r_attri_kept,  show_progress=False)
    '''
    year_block = em.BlackBoxBlocker()
    year_block.set_black_box_function(compare_car_year)
    year_block_result = year_block.block_tables(cars_com_downsampled, market_check_downsampled,
    l_output_attrs=l_attri_kept, r_output_attrs=r_attri_kept, show_progress=False)
    '''

    # combine all blocking results
    block_result = em.combine_blocker_outputs_via_union([brand_block_result, year_block_result])

    print("Number of tuples after blocking: {}".format(len(block_result)))


if __name__ == "__main__":
    main()

