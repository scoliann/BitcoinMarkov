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




