import numpy as np
import pandas as pd
import sys
import os
import argparse
from optparse import OptionParser


import pickle
from HierStack import hierarchy as hie
from HierStack import model as mo
from HierStack import classification as cl


def main(algorithm, data):
	model_filepath = 'Models/'
	output_filepath = 'Output'
	metrics_filename = 'result.txt'

	if not os.path.isdir(output_filepath):
		os.mkdir(output_filepath)
	
	pkl_filename = "ClassifyTE.pkl"
	fd = open(os.path.join(output_filepath, metrics_filename), 'w')



	test_label = pd.DataFrame(data['classification'])
	test_data = pd.DataFrame(data.drop('classification', axis=1))

	parent_classifiers = {}

	with open(model_filepath + pkl_filename, 'rb') as fb:
		parent_classifiers = pickle.load(fb)

	m = mo.model(h, algorithm)
	print("---------------------------Starting to Test the model--------------------")
	m.test_model(test_data, test_label, parent_classifiers)
	print("----------------------------Done with testing model-----------------------")

	# ---------------- Write fold-wise results to a file ---------------------

	fd.write('hierarchical evaluation metrics for testing dataset')
	fd.write('\nPrecision: ' + str(m.precision[-1]))
	fd.write('\nRecall: ' + str(m.recall[-1]))
	fd.write('\nF-measure: ' + str(m.hf[-1]))
	fd.write('\n\nEvaluation per level')

	for i in range(len(m.precision_level[-1])):
		fd.write('\nPrecision Level ' + str(i+1) + ' \t ' + str(m.precision_level[-1][i]))
		fd.write('\nRecall Level ' + str(i+1) + ' \t ' + str(m.recall_level[-1][i]))
		fd.write('\nF-measure Level ' + str(i+1) + ' \t ' + str(m.hf_level[-1][i]))
		fd.write('\n------------------------------------------------------------------------------------------------------')
    

	fd.write('\n\n================================================================================================================================\n')
    


	output_filename = "predicted_result.txt"
	f = open(os.path.join(output_filepath, output_filename) ,'w')
	f.write('true \t predicted\n')
	for i in range(len(m.labels_test)):
		f.write(str(m.labels_test[i][0]) +  '\t ' + str(m.labels_test[i][1]) + '\n')
	f.close()

	return m.labels_test


if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-f", "--filename", dest="filename", help="Name of the training file.")
	parser.add_option("-n", "--nodes_filepath", dest="nodes_filepath", help="Path to node filelist.")
	

	parser.add_option("-a", "--algorithm", dest="algorithm", help="Hierarchical classification algorithm LCPNB or nLLCPN.", default='lcpnb')

	(options, args) = parser.parse_args()
   
	dataset_filepath = "./data/"

	hier_label = {}
	h = hie.hierarchy(options.nodes_filepath)

	with open(dataset_filepath + options.filename , "r") as csvfile:
		data = pd.read_csv(csvfile, low_memory=False)

	X = data.iloc[:, 0:(pow(4,2) + pow(4,3) + pow(4,4))]
	Y = data.iloc[:,-1]
	train_data = pd.concat([X, Y], axis=1)

	hier_label = main(options.algorithm, train_data)

	# for i in range(len(hier_label)):
	# 	print("The predicted hierarchy is \n")
	# 	print(str(hier_label[i][1]))
	print("Done Testing given dataset")