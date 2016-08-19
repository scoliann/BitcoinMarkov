import sys
import shutil
import os


def readParameters(parameterKey):

	# Scan through file to find parameterKey
	parameterKeyCounter = 0
	with open('parameters.txt', "r") as ifile:
		for line in ifile:
			line = line.rstrip().split('\t')

			# If parameterKey is found
			if line[0] == parameterKey:

				# Increment parameterKeyCounter
				parameterKeyCounter += 1

				# Get the data type and read in the data
				dataType = line[1]
				if dataType == "string":
					parameterValue = line[2]
				elif dataType == "list":
					parameterValue = line[2].split(',')
				elif dataType == "int":
					parameterValue = int(line[2])

	# If only one parameterKey was found, then return
	if parameterKeyCounter == 1:
		return parameterValue
	else:
		sys.exit("ERROR:\t" + parameterKey +  " in parameters.txt must occur exactly once.")


def createEmptyDirectory(fileName):

	# If fileName exists, delete and remake it.  Else delete it.
	try:
		shutil.rmtree(fileName)
		os.makedirs(fileName)
	except:
		os.makedirs(fileName)
