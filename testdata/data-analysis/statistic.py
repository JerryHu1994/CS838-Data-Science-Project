"""
Univertity of Wisconsin-Madison
Yaqi Zhang
"""
import sys
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    '''analyze the number of words in names'''
    if len(sys.argv) != 2:
        print("Usage: python %s <namefile>" % (sys.argv[0]))
        sys.exit(1)
    filename  = sys.argv[1]
    with open(filename) as f:
        names = f.readlines()
    sizes = [len(item.split()) for item in names]
    plt.hist(np.array(sizes))
    plt.show()
