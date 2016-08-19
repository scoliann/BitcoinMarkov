import functionModule as fm


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

	return ilist


def saveDataSetAsCSV(btcClassHistory, d):

	# Save the date in btcClassHistory as a CSV
	text_file = open('datasets/' + d + '.csv', "a")
	for entry in btcClassHistory:
		line = entry[0] + ',' + str(entry[1])
		text_file.write(line + "\n")
	text_file.close()
	
	
if __name__ == "__main__":

	# Read in the parameters from "parameters.txt"
	btcPriceHistoryFileName = fm.readParameters("completePriceHistoryFile")
	dValueList = fm.readParameters("listOfDValues")

	# Read in the bitcoin price history & change strings to float
	btcPriceHistory = readKeyValueCSV(btcPriceHistoryFileName)
	btcPriceHistory = [(ituple[0], float(ituple[1])) for ituple in btcPriceHistory]

	# If "datasets" exists, delete it and its contents, and remake it.  Else, make it.
	fm.createEmptyDirectory('datasets')

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
			if priceJ > (float(d) * priceI):
				btcClassHistory.append((btcPriceHistory[date][0], 'UP'))
			else:
				btcClassHistory.append((btcPriceHistory[date][0], 'DOWN'))

		# Save each dataset to folder named "datasets"
		saveDataSetAsCSV(btcClassHistory, d)







			
