#!/usr/bin/env python3
"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: >> python {} <feature_file>".format(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        lines = f.readlines()
    # words = [line.split(", ")[0] for line in lines]
    words = []
    for line in lines:
        temp = line.split(", ")[0]
        words.extend(temp.split())
    lst = [[int(token) for token in line.split(", ")[1:]] for line in lines]
    # lst = [sub_list for sub_list in lst if len(sub_list) == 7]
    M = np.array(lst)
    x = M[:, 0:-1]
    y = M[:, -1]

    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1
    sorted_words = [(k, word_count[k]) for k in sorted(word_count, key=word_count.get, reverse=True)]
    out_filename = filename.split('.')[0] + "_frequency.dat"
    out_file = open(out_filename, 'w')
    for word, frequency in sorted_words:
        out_file.write("{} : {}\n".format(word, frequency))
    out_file.close()
