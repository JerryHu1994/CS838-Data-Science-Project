#!/usr/bin/env python3
"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

def has_numbers(string):
    return any(char.isdigit() for char in string)

def has_parenthese(string):
    for char in string:
        if char in ['(', ')']:
            return True
    else:
        return False

if __name__ == "__main__":
    '''prune test negative samples in test_negative.dat
       then pick samples randomly according to frequency and write them
       to test_negative_pruned.dat
    '''
    n_samples = 850
    filename = "test_negative.dat"
    out_filename = "test_negative_pruned.dat"
    blacklist = set()
    with open("blacklist.dat", 'r') as f:
        lines = f.readlines()
    for line in lines:
        blacklist.add(line.strip())
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    count = 0
    lst = []
    lens = set()
    for line in lines:
        word = line.split(", ")[0]
        tokens = word.lower().split()
        for token in tokens:
            if token in blacklist or has_numbers(token) or has_parenthese(token):
                break
        else:
            lens.add(len(tokens))
            lst.append(line)
            count += 1
    print("negative sample are pruned from {:d} to {:d}".format(len(lines), count))
    picked = random.sample(lst, n_samples)
    with open(out_filename, 'w') as f:
        for line in picked:
            f.write(line + "\n")
    print("write {:d} samples to {}".format(len(picked), out_filename))
