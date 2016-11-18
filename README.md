## Inspiration
After reading an academic paper about using Twitter sentiment to predict the stock market (https://arxiv.org/pdf/1010.3003.pdf), I became interested in the application of data mining, machine learning, game theory, etc. to gain a competitive edge.  The market that I have chosen to explore is that of bitcoin.  The reason is twofold:
- 1) Cryptocurrencies can be traded instantly with low fees (around 0.02%).
- 2) Cryptocurrencies are subject to constant fluctuation, and therefore there is a consistent potential to make money.  No potential would exist if the price of BTC was constant.
I believe that it is best to start off small. Therefore, my first goal is to determine if the behavior of bitcoin can be expressed meaningfully using a markov chain.

## Experiment Details
To read my application of the scientific method (question, hypothesis, procedure, experiment, etc.) to this project, read the included PDF.

## Prerequisites
- 1) Download the price history of bitcoin from http://www.coindesk.com/price/.  
- 2) Clean the data so that only dates and prices (and nothing else) remain.  
- 3) Populate the "completePriceHistoryFile" line of parameters.txt with the file name of your price history CSV file.  
- 4) Populate the "minStatSignificantSize" line of parameters.txt with the minimum acceptable statistically significant sample size.
To recreate my results, follow the procedure outlined in the included PDF.  If at any time you find something confusing, read the included PDF.

## Relevant Files
- 1) assignClasses.py takes a CSV of bitcoin's price history as input.  It outputs six CSV files into the "datasets" folder (one dataset for each value of d).
- 2) recordTransitions.py takes the CSV files in the "datasets" folder as input.  It outputs a folder called "transitions".  "transitions" contains subfolders for each CSV file from "datasets" that was read in as input.  These subfolders contain subfolders called "UP" and "DOWN".  "UP" and "DOWN" contain CSV files for transitions from the UP and DOWN states.

## Running Scripts
The scripts should be run in the following order using the following syntax:
- 1) python assignClasses.py
- 2) python recordTransitions.py

## Statistical Mishaps
One of the central goals of this experiment is to determine a statistical measure to prove the validity of the results.  To summarize the experiment simply, we are:
- 1) Taking the data and labeling each time period as "UP" or "DOWN" depending on if the price of bitcoin went up or down.
- 2) Calculating the probability of "UP" given some number of past probabilities (eg. probability of "UP" given that the previous day was a "DOWN", etc.) for the ENTIRE dataset.
- 3) Statistically test if the calculated probability of "UP" is internally consistent with the subsets within the dataset.

This creates a problem.  The probability of "UP" calculated in step 2 above might be 0.5.  However, when checking if this probability is internally consistent within the subsets of the dataset, one might find that the probability of "UP" for the first half of the time series data set is 0.8 and the probability of "UP" for the second half of the time series data set is 0.2.  This would obviously warrant suspicion that the initial calculation of p(UP) = 0.5 is unusable as it is obvious that p(UP) is changing over the course of the time series.  What, however, should one think if p(UP) for the first half was 0.45 and p(UP) for the second half was 0.55.  This situation is less obvious.  The problem here is that the calculated p(UP) for the subsets will (in all likelihood) indicate that the underlying process is non-stationary.  After consulting a friend who is getting a Ph.D. in Statistics, I have come to the conclusion that testing whether the deviations of p(UP) for the subsets are significantly different from p(UP) for the main set will be very difficult.  I certainly do not know how to, and neither did my friend.  There are a variety of tests that we could apply here, but the nature of this experiment would undermine their validity, as they rely on assumptions such as each data point being independent, etc.  I originally began my bitcoin research with Markov chains because I thought that it would be simple.  Now, I must end this line of investigation for the following reasons:

- 1) I will be unable to statistically validate my results for the aforementioned reasons.
- 2) There are other approaches to analyzing bitcoin that need to be tried.
- 3) The probability that p(UP) for the entire data set would NOT obviously differ from p(UP) of the subsets seems very slim to me.  And if this difference is to be expected, then there is definitely no reason to continue.  Even if I had the statistical know-how to do so, this phenomena would surely lead to the conclusion that Markov chains are no good for price prediction due to their non-stationary nature.







