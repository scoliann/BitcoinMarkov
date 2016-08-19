import os
import collections as cl
import numpy as np
import scipy.stats
import functionModule as fm


if __name__ == "__main__":

	# Read in the parameters from parameters.txt 
	listOfDValues = fm.readParameters("listOfDValues")

	# Make folder named "transitionProbabilities"
	fm.createEmptyDirectory('transitionProbabilities')

	# Make subfolders in "transitionProbabilities" for all dValues in listOfDValues.  In each subfolder, make folders "UP" and "DOWN".
	for dValue in listOfDValues:
		os.makedirs('transitionProbabilities/' + dValue + '/UP')
		os.makedirs('transitionProbabilities/' + dValue + '/DOWN')

	# Read in CSV files from "transitions" one by one and apply binomial testing
	for dValueDirectory in os.listdir('transitions'):
		for upDownDirectory in os.listdir('transitions/' + dValueDirectory):
			for fileName in os.listdir('transitions/' + dValueDirectory + '/' + upDownDirectory):

				# Check that ifile is a file
				if os.path.isfile('transitions/' + dValueDirectory + '/' + upDownDirectory + '/' + fileName):

					# Read in the CSV, counting transitions
					transitionCounts = cl.defaultdict(float)
					firstDate = "no firstDate"
					lastDate = "no endDate"
					skipFirstLine = True
					with open('transitions/' + dValueDirectory + '/' + upDownDirectory + '/' + fileName, "r") as ifile:
						for line in ifile:
							# Skip the first line which contains titles
							if skipFirstLine:
								skipFirstLine = False
								continue
							line = line.rstrip().split(',')

							# Get variables from CSV line
							date = line[0]
							startState = line[1]
							endState = line[2]

							# Increment the count for the given transition
							transitionName = startState + "_to_" + endState
							transitionCounts[transitionName] += 1.0

							# Update firstDate if appropriate
							if firstDate == "no firstDate":
								firstDate = date

							# Update lastDate
							lastDate = date

					# Get the name of the relevant transition
					if 'UP_to_UP' in transitionCounts.keys():
						consideredTransition = 'UP_to_UP'
					elif 'DOWN_to_DOWN' in transitionCounts.keys():
						consideredTransition = 'DOWN_to_DOWN'

					# Prepare the CSV file for the data to be saved to it
					binomialCSVFile = fileName.split('.csv')[0] + '_binomial.csv'
					text_file = open('transitionProbabilities/' + dValueDirectory + '/' + upDownDirectory + '/' + binomialCSVFile, "a")
					titleLine = "p,p-value"
					text_file.write(titleLine + "\n")

					# Apply the binomial test for all values in {0.00, 0.01, 0.02, ..., 1.00}
					for p in np.arange(0.00, 1.01, 0.01):
						
						# Apply the binomial test
						numberOfSuccesses = transitionCounts[consideredTransition]
						numberOfTrials = sum(transitionCounts.values())
						pValue = scipy.stats.binom_test(numberOfSuccesses, numberOfTrials, p)

						# Construct CSV line and save it
						csvLine = str(p) + ',' + str(pValue)
						text_file.write(csvLine + "\n")

					text_file.close()





