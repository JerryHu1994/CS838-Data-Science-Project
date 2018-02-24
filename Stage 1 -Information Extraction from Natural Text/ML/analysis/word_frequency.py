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
    '''extract words from feature_file and
       output the word and its frequency
       in descending order to frequency file
    '''
    if len(sys.argv) != 2:
        print("Usage: >> python {} <feature_file> ".format(sys.argv[0]))
        sys.exit(1)
    feature_file = sys.argv[1]
    with open(feature_file, 'r') as f:
        lines = f.readlines()
    words = []
    for line in lines:
        temp = line.split(", ")[0]
        words.extend(temp.split())
    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1
    sorted_words = [(k, word_count[k]) for k in sorted(word_count, key=word_count.get, reverse=True)]
    out_filename = feature_file.split('.')[0] + "_frequency.dat"
    out_file = open(out_filename, 'w')
    for word, frequency in sorted_words:
        out_file.write("{} : {}\n".format(word, frequency))
    out_file.close()
    print("writing word and cooresponding frequency to {}".format(out_filename))
