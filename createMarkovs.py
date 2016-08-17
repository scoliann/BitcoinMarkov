import os
import collections as cl
import shutil


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


def resetDirectory(dirName):
	if os.path.exists(dirName):
		rmFiles = [f for f in os.listdir(dirName) if os.path.isfile(dirName + '/' + f)]
		for rmFile in rmFiles: 
			os.remove(dirName + '/' + rmFile)
	else:
		os.makedirs(dirName)


def readKeyValueCSV(fileName):

	# Open the CSV
	ilist = []
	with open(fileName, "r") as ifile:
		for line in ifile:
			line = line.rstrip().split(',')

			# Record the price history
			key = line[0]
			value = line[1]
			ilist.append((key, value))

	# Return the list
	return ilist


def getTransitionCounts(startIndex, endIndex, btcPriceHistory, transitionCountRecord):

	# The base case (when startIndex == 0)
	if startIndex == 0:

		# Get the initial transition count between startIndex and endIndex
		for index in range(startIndex, endIndex):
		
			# Get the present state and future state
			presentState = btcPriceHistory[index][1]
			futureState = btcPriceHistory[index + 1][1]

			# Count all the different transitions
			if (presentState == 'UP') and (futureState == 'UP'):
				transitionCountRecord[(startIndex, endIndex)]['upToUp'] += 1.0
			elif (presentState == 'UP') and (futureState == 'DOWN'):
				transitionCountRecord[(startIndex, endIndex)]['upToDown'] += 1.0
			elif (presentState == 'DOWN') and (futureState == 'UP'):
				transitionCountRecord[(startIndex, endIndex)]['downToUp'] += 1.0
			elif (presentState == 'DOWN') and (futureState == 'DOWN'):
				transitionCountRecord[(startIndex, endIndex)]['downToDown'] += 1.0

	# In the non-base case, iterate over the data
	else:

		# Calculate values to remove for each transition
		removeValues = cl.defaultdict(float)
		if (btcPriceHistory[startIndex - 1][1] == 'UP') and (btcPriceHistory[startIndex][1] == 'UP'):
			removeValues['upToUp'] = 1
		elif (btcPriceHistory[startIndex - 1][1] == 'UP') and (btcPriceHistory[startIndex][1] == 'DOWN'):
			removeValues['upToDown'] = 1
		elif (btcPriceHistory[startIndex - 1][1] == 'DOWN') and (btcPriceHistory[startIndex][1] == 'UP'):
			removeValues['downToUp'] = 1
		elif (btcPriceHistory[startIndex - 1][1] == 'DOWN') and (btcPriceHistory[startIndex][1] == 'DOWN'):
			removeValues['downToDown'] = 1

		# Calculate values to add for each transition
		addValues = cl.defaultdict(float)
		if (btcPriceHistory[endIndex - 1][1] == 'UP') and (btcPriceHistory[endIndex][1] == 'UP'):
			addValues['upToUp'] = 1
		elif (btcPriceHistory[endIndex - 1][1] == 'UP') and (btcPriceHistory[endIndex][1] == 'DOWN'):
			addValues['upToDown'] = 1
		elif (btcPriceHistory[endIndex - 1][1] == 'DOWN') and (btcPriceHistory[endIndex][1] == 'UP'):
			addValues['downToUp'] = 1
		elif (btcPriceHistory[endIndex - 1][1] == 'DOWN') and (btcPriceHistory[endIndex][1] == 'DOWN'):
			addValues['downToDown'] = 1

		# Calculate new transition counts and add to transitionCountRecord
		for transition in ['upToUp', 'upToDown', 'downToUp', 'downToDown']:

			# The baseValues are the transition counts from previous markov chain
			#	All but the value at smallest index in baseValues are used in the calculation of current transition probabilities
			baseValues = transitionCountRecord[((startIndex - 1), (endIndex - 1))][transition]

			# We subtract out the unused value and add in the new value
			transitionCountRecord[(startIndex, endIndex)][transition] = baseValues - removeValues[transition] + addValues[transition]

	# Return the transition counts
	return transitionCountRecord


def getTransitionProbability(startIndex, endIndex, transitionCountRecord):

	# Calculate the probabilities of all the transitions
	transitionProb = cl.defaultdict(float)
	for transition in transitionCountRecord[(startIndex, endIndex)]:

		# Round transition probability to three decimal places
		transitionProbability = transitionCountRecord[(startIndex, endIndex)][transition] / (endIndex - startIndex + 1)
		transitionProb[transition] = round(transitionProbability, 3)

	# Return the transition probabilities
	return transitionProb


def saveDataAsCSV(text_file, subsetTransitionProb):

	# Record the transition probabilities
	for transition in subsetTransitionProb:

		# Construct CSV line and save
		line = str(size) + "," + transition + "," + str(subsetTransitionProb[transition]) + "," + btcPriceHistory[startIndex][0] + "," + btcPriceHistory[endIndex][0]
		text_file.write(line + "\n")


if __name__ == "__main__":

	# Read in the parameter for minimum size of statistical significance
	minStatSignificantSize = readParameters("minStatSignificantSize")
	
	# If transprob exists, delete it and its contents, and remake it.  Else, make it.
	resetDirectory('transprob')

	# Read in CSV files from datasets folder
	for ifile in os.listdir('datasets'):
		if os.path.isfile('datasets/' + ifile):
			btcPriceHistory = readKeyValueCSV('datasets/' + ifile)

			# Prepare CSV file for data to be saved to it
			transitionFileName = "trans_" + ifile
			text_file = open('transprob/' + transitionFileName, "a")
			titleLine = "size,transition,transitionProb,startDate,endDate"
			text_file.write(titleLine + "\n")

			# Create a variable to record transition probabilities so that they don't have to be recalculated every time
			transitionCountRecord = cl.defaultdict(lambda: cl.defaultdict(float))

			# Iterate over all valid subset sizes in price history data set
			for size in range(minStatSignificantSize, len(btcPriceHistory) + 1):

				# Iterate over all subsets of that size in price history data set
				startIndex = 0
				endIndex = size

				while endIndex < len(btcPriceHistory):

					# Get the updated transition counts
					transitionCountRecord = getTransitionCounts(startIndex, endIndex, btcPriceHistory, transitionCountRecord)

					
					for startStop in transitionCountRecord:

						print "\t" + str(transitionFileName)
						print "\t" + str(startStop)

						for transition in transitionCountRecord[startStop]:

							print transition + '\t' + str(transitionCountRecord[startStop][transition])

					###print str(ifile)
					###import sys
					##sys.exit()

					# Calculate the transition probability
					subsetTransitionProb = getTransitionProbability(startIndex, endIndex, transitionCountRecord)

					# Record the transition probabilities in the CSV file for the given dataset
					saveDataAsCSV(text_file, subsetTransitionProb)

					# Increment startIndex and endIndex
					startIndex += 1
					endIndex += 1

			text_file.close()








