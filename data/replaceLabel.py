#!/usr/bin/python
import sys
import os

def main():
	if len(sys.argv) != 3:
		print "Error: Please give an input name and an output name."
	folderName = sys.argv[1]
	outputName = sys.argv[2]
	filelist = os.listdir(folderName)

	#loop through the file list, open each file, replace $$$
	for i in filelist:
		inputpath = "./"+folderName+"/"+i
		filecontent = open(inputpath, 'r').read()
		filecontent = filecontent.replace('&&&', '<person>')
		filecontent = filecontent.replace('$$$', '</person>')
		
		outdir = "./"+outputName
		outputPath = "./" + outputName + "/" + i
		if not os.path.exists(outdir):
			os.makedirs(outdir)
		f = open(outputPath, 'w+')
		f.write(filecontent)
		f.close()
		print i +' finished'

if __name__ == "__main__":
	main()

