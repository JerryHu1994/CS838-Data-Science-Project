#!/usr/bin/env python
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu
##################################
# This script reads a directory of text documents with human names labeled as <person>name</name>, and then
# generate both positive and negative sample for both training and testing dataset. The output will get
# saved into a dat file with following format:
# [name string, string length, isCapitalized, postion index from sentence head, sentence length, ended with
# certain pattern, prefixed with certain pattern]
# eg: Jieru Hu, 2, 1, 0, 8, 1, 0
import sys
import os
import re
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

# Returns a list of positive samples, given a sentence string
def extractPositiveFeature(line):
    featureList = []
    names = re.findall(r"<person>[^<]*</person>", line)

    # replace <person>name</person> with <person> for the easieness of index counting
    replacedLine = re.sub(r"<person>[^<]*</person>", '<person>', line)
    replacedLineList = replacedLine.split()
    # save all the indexes of matched names
    nameIdxlist = [ind for ind, val in enumerate(replacedLineList) if val == '<person>']

    #print (replacedLine)
    preCount = 0 # preCount stores the difference between the length of the replacedLineList and it original
    list
    for ind, name in enumerate(names):
        nameStr = name[8:-9] # save the name string
        lengthStr = str(len(nameStr.split())) # save the length string
        capitalizedStr = checkCapitalized(nameStr) # save the capitalized boolean string

        headPositionStr = str(nameIdxlist[ind] + preCount) # save the position from head
        preCount += int(lengthStr) - 1
        lineLengthStr = str(len((line.replace('<person>', '').replace('</person>', '').split()))) # save the sentence length string

        endStr = checkEndMatch(replacedLineList, nameIdxlist[ind]) # save the end-pattern boolean string
        prefixStr = checkPrefixMatch(replacedLineList, nameIdxlist[ind]) # save the prefix-pattern boolean string

        features = [nameStr, lengthStr, capitalizedStr, headPositionStr, lineLengthStr, endStr, prefixStr]
        featureStr = ', '.join(features)

        featureList.append(featureStr)
    return featureList

# Returns a list of negative samples, given a sentence string
def extractNegativeFeature(line):
    nameIdxDict = [] # stores a list of [startIndex, endIndex] set for each labeled name
    names = re.findall(r"<person>[^<]*</person>", line)
    # replace <person>name</person> with <person> for the easieness of index counting
    replacedLine = re.sub(r"<person>[^<]*</person>", '<person>', line)
    replacedLineList = replacedLine.split()
    # save all the indexes of matched names
    nameIdxlist = [ind for ind, val in enumerate(replacedLineList) if val == '<person>']
    preCount = 0 # preCount stores the difference between the length of the replacedLineList and it original
   
    # save all tagged name index pairs
    for ind, name in enumerate(names):
        nameStr = name[8:-9] # save the name string
        currLen = len(nameStr.split())
        nameIdxDict.append((nameIdxlist[ind] + preCount, nameIdxlist[ind]+ preCount + currLen))
        preCount += currLen - 1
    
    wordList = line.replace('<person>', '').replace('</person>', '').split()
    featureList = []
    # loop through different negative lengths
    for l in negLengthList:
        for start in range(0, len(wordList)-l+1):
            startI, endI = start, start+l
            # skip if the currPair is contained by a tagged name
            if inPositive(nameIdxDict, startI, endI): continue
        
            # start producing feature vectors
            nameStr = ' '.join(wordList[startI:endI])#' '.join(i) for i in wordList[startI:endI] # save the name string
            lengthStr = str(l) # save the length string
            capitalizedStr = checkCapitalized(nameStr) # save the capitalized boolean string

            headPositionStr = str(startI) # save the position from head
            lineLengthStr = str(len(wordList)) # save the sentence length string

            endStr = checkEndMatch(wordList, endI-1) # save the end-pattern boolean string
            prefixStr = checkPrefixMatch(wordList, startI) # save the prefix-pattern boolean string

            features = [nameStr, lengthStr, capitalizedStr, headPositionStr, lineLengthStr, endStr, prefixStr]
            featureStr = ', '.join(features)

            featureList.append(featureStr)

    return featureList

# main method
def main():
    # parameter input validation
    if len(sys.argv)!=4:
        print ("[USAGE]: python splitData.py input_dir output_file pos/neg\n")
        sys.exit(1)
    inputDir, outputDir, dataFlag = sys.argv[1], sys.argv[2], sys.argv[3]
    if not (dataFlag == "pos" or dataFlag == "neg"):    
        print ("[USAGE]: python splitData.py input_dir output_file pos/neg\n")
        sys.exit(1)
    dataFlag = True if dataFlag == "pos" else False

    # load prefix and end pattern
    loadPattern(prefixDict, prefixPatternPath)
    loadPattern(endDict, endPatternPath)
    return
    inputFiles = []
    if os.path.exists(inputDir):
        inputFiles = os.listdir(inputDir)
    else:
        print ("[ERROR]: Input directory not exists")
        sys.exit(1)
    outputFile = open(outputDir, 'w')

    #loop through all labeled files
    for fname in inputFiles:
        filePath = inputDir + "/" + fname
        with open(filePath, 'r') as f:
            print ("[INFO]: Finish reading ", filePath, "\n")
            lines = f.read()
            #split the file content given the delimiter
            lineList = re.split(delimiter, lines)
            #split the file contents into strings using certain delimiters
            for line in lineList:
                print (line)
                if dataFlag:
                    if containsName(line):
                        # write all the positive feature vectors into the output file
                        featureList = extractPositiveFeature(line)
                        for feature in featureList:
                            outputFile.write(feature + "\n")
                else:
                    # write all the negative feature vectors into the output file
                    featureList = extractNegativeFeature(line)
                    for feature in featureList:
                        outputFile.write(feature + "\n")
    # close the output file
    outputFile.close()

if __name__ == "__main__":
  main()

