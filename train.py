import numpy as np
import pandas as pd
import sys
import os
import argparse
import time
from optparse import OptionParser
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split

import pickle
from HierStack import hierarchy as hie
from HierStack import model as mo
import HierStack.classification as cl

def main(algorithm, train_data, h, cost, gamma):	
	index = 1
	output_filepath = 'models'
	if not os.path.isdir(output_filepath):
		os.mkdir(output_filepath)

	pkl_filename = "ClassifyTE_combined_" + str(cost) + "_" + str(gamma) + ".pkl"
	print(f'Training ClassifyTE and saving it to "{pkl_filename}" in "{output_filepath}" directory.')
	parent_classifiers = {}
	train_data_parent = pd.DataFrame.copy(train_data)
	train_label = pd.DataFrame(train_data['classification'])
	train_data = pd.DataFrame(train_data.drop('classification',axis=1))

	dataInnerNode = h.getDataFromInnerNodes(train_data_parent)

	m = mo.model(h, algorithm)
	print("----------------Training Started----------------")
	parent_classifiers = m.generate_models(dataInnerNode, index, cost, gamma)
	
	with open(os.path.join(output_filepath, pkl_filename), "wb") as fm:
			pickle.dump(parent_classifiers, fm)


if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-f", "--filename", dest="filename", help="Name of the training file.")
	parser.add_option("-n", "--nodes_filepath", dest="node_file", help="Path to node filelist.", default='node.txt')
	parser.add_option("-c", "--c_value", dest="c_value", help="c parameter for SVM")
	parser.add_option("-g", "--gamma_value", dest="gamma_value", help="gamma parameter for SVM")
	
	# Hierarchical classification algorithm can be either:
	# 		non-Leaf Local Classifier per Parent Node (nLCPN)
	# 		Local Classifier per Parent Node and Branch (LCPNB)

	parser.add_option("-a", "--algorithm", dest="algorithm", help="Hierarchical classification algorithm LCPNB or nLLCPN.", default='lcpnb')

	(options, args) = parser.parse_args()
	dataset_filepath = "./data/"
	node_filepath = "./nodes/"

	h = hie.hierarchy(node_filepath + options.node_file)

	with open(dataset_filepath + options.filename , "r") as csvfile:
		data = pd.read_csv(csvfile, low_memory=False)

	start_time = time.time()
	main(options.algorithm, data, h, options.c_value, options.gamma_value)
	total_time = time.time() - start_time
	print("---------------------------------------------Ending Training--------------------------------------------")
	print("\nTotal time elapsed in minutes\t", total_time/60)

