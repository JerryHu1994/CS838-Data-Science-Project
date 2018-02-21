#!/usr/bin/env python
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu
##################################

import numpy as np
import matplotlib.pyplot as plt

# define set for certain prefix strings
prefixPatternPath = './prefixPattern'
prefixDict = set()

# define set for certain end strings
endPatternPath = './endPattern'
endDict = set()

# define a list contains the all possible length of negative examples
negLengthList = [1, 2, 3]

# define string for sentence breaking
delimiter = '[,.!?;]\s*'

# Load a certain pattern into the global dictionary (predix and end)
def loadPattern(dictset, filename):
    with open(filename, 'r') as f:
        content = f.readlines()
        for line in content:
            dictset.add(line.strip())
    print (dictset)

# Return true if all words in a name is capitalized
def checkCapitalized(name):
    for i in name.split():
        if not i[0].isupper():
            return str(0)
    return str(1)

# Check if linelist[ind] has certain end pattern
def checkEndMatch(linelist, ind):
    if ind < len(linelist) -1:
        if linelist[ind+1] in endDict:
            return '1'
    return '0'

# Check if linelist[ind] has certain prefix pattern
def checkPrefixMatch(linelist, ind):
    if ind > 0:
        if linelist[ind-1] in prefixDict:
            return '1'
    return '0'

# check if the startIndex and endIdx is contained within a positive name
def inPositive(nameDict, startI, endI):
    for name in nameDict:
        if name[0] <= startI and endI <= name[1]:
            return True
    return False

# Returns if the given sentence string contains a name tag
def containsName(line):
   return True if "<person>" in line else False



if __name__ == "__main__":
  main()

