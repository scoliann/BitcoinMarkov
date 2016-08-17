import os
import shutil
import string


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


def getTransitionLists(btcPriceHistory):

	# Create two lists of transitions from UP and transitions from DOWN
	transFromUP = []
	transFromDOWN = []
	for date in range(len(btcPriceHistory) - 1):

		if btcPriceHistory[date][1] == 'UP':
			if btcPriceHistory[date + 1][1] == 'UP':
				date = btcPriceHistory[date][0]
				entry = (date, 'UP', 'UP')
				transFromUP.append(entry)
			elif btcPriceHistory[date + 1][1] == 'DOWN':
				date = btcPriceHistory[date][0]
				entry = (date, 'UP', 'DOWN')
				transFromUP.append(entry)
		elif btcPriceHistory[date][1] == 'DOWN':
			if btcPriceHistory[date + 1][1] == 'UP':
				date = btcPriceHistory[date][0]
				entry = (date, 'DOWN', 'UP')
				transFromDOWN.append(entry)
			elif btcPriceHistory[date + 1][1] == 'DOWN':
				date = btcPriceHistory[date][0]
				entry = (date, 'DOWN', 'DOWN')
				transFromDOWN.append(entry)

	# Return results
	return (transFromUP, transFromDOWN)


def getSublistList(transFromState, minStatSignificantSize):

	sublistTransFromState = []
	for index in range(0, len(transFromState), minStatSignificantSize):

		# If the number of remaining unused indices will be greater than or equal to minStatSignificantSize
		if ((len(transFromState) - 1) - (index + minStatSignificantSize)) >= minStatSignificantSize:
			sublist = transFromState[index : index + minStatSignificantSize]

		# If the number of remaining unused indices will be less than minStatSignificantSize, add those indices to this sublist
		else:
			sublist = transFromState[index : len(transFromState) - 1]

		# Add sublist to list of sublists
		sublistTransFromState.append(sublist)

	# Return results
	return sublistTransFromState


def makeSublistCSVs(sublistTransFromState, dvalue, fromStateName):

	# For each sublist, save its contents into its own CSV file
	for sublist in sublistTransFromState:

		# Prepare the CSV file for the data to be saved to it
		sublistStartDate = string.replace(sublist[0][0].split(' ')[0], '/', '-')
		sublistEndDate = string.replace(sublist[len(sublist) - 1][0].split(' ')[0], '/', '-')
		csvFileName = dValue + '_' + fromStateName + '_' + sublistStartDate + '_' + sublistEndDate + '.csv'

		text_file = open('transitions/' + dValue + '/' + fromStateName + '/' + csvFileName, "a")
		titleLine = "date,from state,to state"
		text_file.write(titleLine + "\n")

		# Save each entry to the CSV file
		for entry in sublist:
			
			# Construct string to save to CSV file
			#	ie. Transform ('date','UP','DOWN') to date,UP,DOWN
			entryStringCSV = string.replace(str(entry)[1:-1], "\'", "")

			# Save entryStringCSV to CSV file
			text_file.write(entryStringCSV + "\n")

		text_file.close()


if __name__ == "__main__":

	# Read in the parameter for minimum size of statistical significance
	minStatSignificantSize = readParameters("minStatSignificantSize")
	
	# If transitions exists, delete it and its contents, and remake it.  Else, make it.
	try:
		shutil.rmtree('transitions')
		os.makedirs('transitions')
	except:
		os.makedirs('transitions')

	# Read in CSV files from datasets folder
	for ifile in os.listdir('datasets'):
		if os.path.isfile('datasets/' + ifile):
			btcPriceHistory = readKeyValueCSV('datasets/' + ifile)

			# Create two lists of transitions from UP and transitions from DOWN
			(transFromUP, transFromDOWN) = getTransitionLists(btcPriceHistory)

			# Break list of transitions from UP and DOWN into sublists of size minStatSignificantSize
			sublistTransFromUP = getSublistList(transFromUP, minStatSignificantSize)
			sublistTransFromDOWN = getSublistList(transFromDOWN, minStatSignificantSize)

			# Create a directory for each dataset.  Each directory contains a subdirectory for the UP and DOWN states.
			dValue = ifile.rsplit('.', 1)[0]
			os.makedirs('transitions/' + dValue + '/UP')
			os.makedirs('transitions/' + dValue + '/DOWN')

			# For each sublist, save its contents into its own CSV file
			makeSublistCSVs(sublistTransFromUP, dValue, 'UP')
			makeSublistCSVs(sublistTransFromDOWN, dValue, 'DOWN')


				










