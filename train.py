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
#from HierStack import classification as cl
import HierStack.classification as cl

def main(algorithm, X, Y):	
	index = 1
	train_data = pd.concat([X, Y], axis=1)

	parent_classifiers = {}
	train_data_parent = pd.DataFrame.copy(train_data)
	train_label = pd.DataFrame(train_data['classification'])
	train_data = pd.DataFrame(train_data.drop('classification',axis=1))

	dataInnerNode = h.getDataFromInnerNodes(train_data_parent)

	m = mo.model(h, algorithm)
	parent_classifiers1 = m.generate_models(dataInnerNode, index)



if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-f", "--filename", dest="filename", help="Name of the training file.")
	parser.add_option("-n", "--nodes_filepath", dest="node_file", help="Path to node filelist.")
	
	# Hierarchical classification algorithm can be either:
	# 		non-Leaf Local Classifier per Parent Node (nLCPN)
	# 		Local Classifier per Parent Node and Branch (LCPNB)

	parser.add_option("-a", "--algorithm", dest="algorithm", help="Hierarchical classification algorithm LCPNB or nLLCPN.", default='lcpnb')

	(options, args) = parser.parse_args()
    #nodes_filepath = sys.argv[1]
	dataset_filepath = "./Data/"
	node_filepath = "./Nodes/"

	h = hie.hierarchy(node_filepath + options.node_file)

	#h = hie.hierarchy(options.nodes_filepath)

	with open(dataset_filepath + options.filename , "r") as csvfile:
		data = pd.read_csv(csvfile, low_memory=False)

#	
	X4 = data.iloc[:, 0:(pow(4,2) + pow(4,3) + pow(4,4))]
	Y = data.iloc[:,-1]

	
	X_train4, X_test4, Y_train4, Y_test4 = train_test_split(X4, Y, test_size=0.15, stratify=Y, random_state=42)

	start_time = time.time()
	main(options.algorithm, X4, Y)
	total_time = time.time() - start_time
	print("---------------------------------------------Ending Training--------------------------------------------")
	print("\nTotal time elapsed in minutes\t", total_time/60)

