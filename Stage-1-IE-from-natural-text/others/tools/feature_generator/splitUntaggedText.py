#!/usr/bin/env python3
##################################
# University of Wisconsin-Madison
# Author: Jieru Hu
##################################
# This script reads a directory of plain text document, and then generate feature vectors for different
# length word combinations, for the purpose of testing.
# [name string, string length, isCapitalized, postion index from sentence head, sentence length, ended with
# certain pattern, prefixed with certain pattern]
# eg: Jieru Hu, 2, 1, 0, 8, 1, 0
import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import splitUtils

# This method extract feature vector from word of different sizes
def extractTestFeature(line):
    featureList = []
    wordList = line.split()
    # loop through different word length
    for l in splitUtils.negLengthList:
        for start in range(0, len(wordList)-l+1):
            startI, endI = start, start+l
            # start producing feature vectors
            nameStr = ' '.join(wordList[startI:endI])#' '.join(i) for i in wordList[startI:endI] # save the name string
            lengthStr = str(l) # save the length string
            capitalizedStr = splitUtils.checkCapitalized(nameStr) # save the capitalized boolean string

            headPositionStr = str(startI) # save the position from head
            lineLengthStr = str(len(wordList)) # save the sentence length string

            endStr = splitUtils.checkEndMatch(wordList, endI-1) # save the end-pattern boolean string
            prefixStr = splitUtils.checkPrefixMatch(wordList, startI) # save the prefix-pattern boolean string

            features = [nameStr, lengthStr, capitalizedStr, headPositionStr, lineLengthStr, endStr, prefixStr]
            featureStr = ', '.join(features)

            featureList.append(featureStr)

    return featureList


# main method
def main():
# parameter input validation
    if len(sys.argv)!=3:
        print ("[USAGE]: python splitUntaggedTest.py input_dir output_file\n")
        sys.exit(1)
    inputDir, outputDir = sys.argv[1], sys.argv[2]

    # load prefix and end pattern
    splitUtils.loadPattern(splitUtils.prefixDict, splitUtils.prefixPatternPath)
    splitUtils.loadPattern(splitUtils.endDict, splitUtils.endPatternPath)
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
            #print ("[INFO]: Finish reading ", filePath, "\n")
            lines = f.read()
            #split the file content given the delimiter
            lineList = re.split(splitUtils.delimiter, lines)
            #split the file contents into strings using certain delimiters
            for line in lineList:
                print (line)
                # write all the combination word feature vectors into the output file
                featureList = extractTestFeature(line)
                for feature in featureList:
                    outputFile.write(feature + "\n")
    # close the output file
    outputFile.close()


if __name__ == "__main__":
  main()

