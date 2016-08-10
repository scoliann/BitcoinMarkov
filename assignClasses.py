import sys
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

	# If only one parameterKey was found, then return
	if parameterKeyCounter == 1:
		return parameterValue
	else:
		sys.exit("ERROR:\t" + parameterKey +  " in parameters.txt must occur exactly once.")


def readPriceHistoryCSV(fileName):

	# Open the CSV
	priceHistory = []
	with open(fileName, "r") as ifile:
		for line in ifile:
			line = line.rstrip().split(',')

			# Record the price history
			date = line[0]
			price = float(line[1])
			priceHistory.append((date, price))

	return priceHistory


def saveDataSetAsCSV(btcClassHistory, d):

	# If folder datasets does not yet exist, create it
	if not os.path.exists('datasets'):
    		os.makedirs('datasets')

	# If the CSV file already exists, delete it
	if os.path.exists('datasets/' + d + '.csv'):
		os.remove('datasets/' + d + '.csv')

	# Save the date in btcClassHistory as a CSV
	text_file = open('datasets/' + d + '.csv', "a")
	for entry in btcClassHistory:
		line = entry[0] + ',' + str(entry[1])
		text_file.write(line + "\n")
	text_file.close()
	
	
if __name__ == "__main__":

	# Read in the parameters from parameters.txt
	btcPriceHistoryFileName = readParameters("completePriceHistoryFile")
	dValueList = [float(i) for i in readParameters("listOfDValues")]

	# Read in the bitcoin price history
	btcPriceHistory = readPriceHistoryCSV(btcPriceHistoryFileName)

	# Create a dataset for each d value
	for d in dValueList:

		# Assign the class values
		btcClassHistory = []
		for date in range(len(btcPriceHistory) - 1):

			# Price on day i
			priceI = btcPriceHistory[date][1]

			# Price on day i+1
			priceJ = btcPriceHistory[date + 1][1]

			# Assign class
			if priceJ > (d * priceI):
				btcClassHistory.append((btcPriceHistory[date][0], 'UP'))
			else:
				btcClassHistory.append((btcPriceHistory[date][0], 'DOWN'))

		# Save each dataset to folder named "datasets"
		saveDataSetAsCSV(btcClassHistory, str(d))

	#---To be continued---







			
