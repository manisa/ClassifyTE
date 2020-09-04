import numpy as np
import pandas as pd
import sys
import os
import time
import argparse
from optparse import OptionParser
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split


import pickle
from HierStack import hierarchy as hie
from HierStack import model as mo
from HierStack import lcpnb as cl
from HierStack.stackingClassifier import *

def main(algorithm, data):
	# ------------------------- Generate hierarcical classification for the sequence-----------------------------
	model_filepath = "models/"
	output_filepath = "output/"
	pkl_filename = "ClassifyTE.pkl"

	test_data = data.iloc[:, 0:(pow(4,2) + pow(4,3) + pow(4,4))]
	test_label = data.iloc[:,-1]

	#test_label = pd.DataFrame(test_data['classification'])
	#test_data = pd.DataFrame(test_data.drop('classification', axis=1))

	parent_classifiers = {}

	with open(model_filepath + pkl_filename, 'rb') as fb:
		parent_classifiers = pickle.load(fb)

	print("---------------------------------------------Evaluation Started---------------------------------------------\n")
	m = mo.model(h, algorithm)

	m.evaluate_model(test_data, parent_classifiers)

	output_filename = "predicted_result.txt"
	f = open(os.path.join(output_filepath, output_filename) ,'w')
	f.write('predicted\t' + "class_name\n")
	for i in range(len(m.labels_test)):
		#f.write(str(m.labels_test[i][0]) +  '\t ' + str(m.labels_test[i][1]) + '\n')
		f.write(str(m.labels_test[i][1]) + '\t' + "LTR\n")
	f.close()

	return m.labels_test



if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-f", "--filename", dest="filename", help="Name of the training file.")
	parser.add_option("-n", "--node_file", dest="node_file", help="Path to node filelist.", default="node.txt")
	
	# Hierarchical classification algorithm can be either:
	# 		non-Leaf Local Classifier per Parent Node (nLCPN)
	# 		Local Classifier per Parent Node and Branch (LCPNB)

	parser.add_option("-a", "--algorithm", dest="algorithm", help="Hierarchical classification algorithm LCPNB or nLLCPN.", default='lcpnb')

	(options, args) = parser.parse_args()

	dataset_filepath = "./data/"
	node_filepath = "./nodes/"

	h = hie.hierarchy(node_filepath + options.node_file)
	start_time = time.time()

	with open(dataset_filepath + options.filename , "r") as csvfile:
		data = pd.read_csv(csvfile, low_memory=False)


	hier_label = {}
	hier_label = main(options.algorithm, data)
	for i in range(len(hier_label)):
		print("The predicted hierarchy is \t")
		print(str(hier_label[i][1]))
	
	elapsed_time = time.time() - start_time
	print("\nTotal time elapsed in seconds\t", elapsed_time)
	print("---------------------------------------------Done with Classification. Open Output folder to view the output file.---------------------------------------------")

