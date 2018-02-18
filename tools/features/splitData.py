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

# define set for prefix and end strings
endDict = set(['Jr', 'Sr', '\'s'])
prefixDict = set(['Mr', 'Ms'])

# define string for sentence breaking
delimiter = '[,.!?;]\s*'

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
    tempLine = line.replace('<person>', ' ').replace('</person>', ' ')
    preCount = 0
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

        #print (featureStr)
        featureList.append(featureStr)
    return featureList

# Returns a list of negative samples, given a sentence string
def extractNegativeFeature():
    return

# Returns if the given sentence string contains a name tag
def containsName(line):
   return True if "<person>" in line else False

# main method
def main():
    # parameter input validation
    if len(sys.argv)!=4:
        print ("[USAGE]: python splitData.py input_dir output_file pos/neg\n")
    inputDir, outputDir, dataFlag = sys.argv[1], sys.argv[2], sys.argv[3]
    if not (dataFlag == "pos" or dataFlag == "neg"):    
        print ("[USAGE]: python splitData.py input_dir output_file pos/neg\n")
    dataFlag = True if dataFlag == "pos" else False


    inputFiles = []
    if os.path.exists(inputDir):
        inputFiles = os.listdir(inputDir)
    else:
        print ("[ERROR]: Input directory not exists")
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
                #print (line)
                if dataFlag:
                    if containsName(line):
                        # write all the positive feature vectors into the output file
                        featureList = extractPositiveFeature(line)
                        for feature in featureList:
                            outputFile.write(feature + "\n")
                else:
                    if not containsName(line):
                        # write all the negative feature vectors into the output file
                        featureList = extractNegativeFeature(line)
                        for feature in featureList:
                            outputFile.write(feature + "\n")
    # close the output file
    outputFile.close()


if __name__ == "__main__":
  main()

