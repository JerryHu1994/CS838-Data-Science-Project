"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import sys
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

def words_count(names):
    '''analyze the number of words in names'''
    sizes = [len(item.split()) for item in names]
    n = len(sizes)
    counts = Counter(sizes)
    print("# occurence\tpercentage")
    for item in counts.items():
        print("{:1d}: {:6d}\t{:7.6f}".format(item[0], item[1], item[1]/n*100.0))
    plt.hist(np.array(sizes))
    plt.show()


def analyze_familynames(names):
    surname_lst = []
    for name in names:
        lst = name.split()
        if len(lst) != 1:
            surname_lst.append(lst[-1])
    counts = Counter(surname_lst)
    for item in counts.items():
        print("{}: {}".format(*item))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python %s <namefile>" % (sys.argv[0]))
        sys.exit(1)
    filename  = sys.argv[1]
    with open(filename) as f:
        names = f.readlines()
    # words_count(names)
    analyze_familynames(names)
