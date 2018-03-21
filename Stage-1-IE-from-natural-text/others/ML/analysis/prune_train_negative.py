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


def main():
    '''prune training negative samples
       then pick samples randomly according to frequency and write them
       to pruned file
    '''
    if len(sys.argv) != 4:
        print("Usage: >> python {} <in_filename> <out_filename> <black_filename>".format(sys.argv[0]))
        sys.exit(1)
    # pick 1500 negative samples, 660 single word, 795 double words, 45 triple word
    numbers = [660, 795, 45] 
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    black_filename = sys.argv[3]
    blacklist = set()
    with open(black_filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        blacklist.add(line.strip())
    print("load {} words from {}".format(len(blacklist), black_filename))
    with open(in_filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    count = 0
    lst = [[], [], []]
    lens = set()
    for line in lines:
        word = line.split(", ")[0]
        tokens = word.lower().split()
        for token in tokens:
            if token in blacklist or has_numbers(token) or has_parenthese(token):
                break
        else:
            lens.add(len(tokens))
            lst[len(tokens) - 1].append(line)
            count += 1
    print("negative sample are pruned from {:d} to {:d}".format(len(lines), count))
    picked = []
    picked.extend(random.sample(lst[0], numbers[0]))
    picked.extend(random.sample(lst[1], numbers[1]))
    picked.extend(random.sample(lst[2], numbers[2]))
    with open(out_filename, 'w') as f:
        for line in picked:
            f.write(line + "\n")
    print("write {:d} samples to {}".format(len(picked), out_filename))



if __name__ == "__main__":
    main()
