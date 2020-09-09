import numpy as np
import pandas as pd
import sys
import os
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

def main(algorithm, X, Y, C, gamma):
	#------------------------ create file to store overall results --------------------------
	output_filepath = 'output'
	if not os.path.isdir(output_filepath):
		os.mkdir(output_filepath)
	output_filename = 'result_' + '.txt'

	fd = open(os.path.join(output_filepath, output_filename), 'w')


	# ------------------------- Generate ML Models and test them using train_test_split . -----------------------------
	
	#cv = StratifiedKFold(n_splits=10)
	data = pd.concat([X, Y], axis=1)
	index = 1
	Y = pd.DataFrame(data['classification'])
	X = pd.DataFrame(data.drop('classification', axis=1))

		
	parent_classifiers = {}
	dataInnerNode = h.getDataFromInnerNodes(data)
	m = mo.model(h, algorithm)

	parent_classifiers = m.generate_models(dataInnerNode, index)

	input_filepath = 'models/'
	pkl_filename = "ClassifyTE.pkl"
	
	with open(input_filepath + pkl_filename, 'rb') as fb:
		parent_classifiers = pickle.load(fb)

	m.test_model(X, Y, parent_classifiers)


	# ---------------- Write fold-wise results to a file ---------------------

	fd.write('FOLD: ' + str(index))
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
    
	
	
	fold_output_filename = "fold" + str(index) + "_labels_test_" + ".txt"
	f = open(os.path.join(output_filepath, fold_output_filename) ,'w')
	f.write('true \t predicted\n')
	for i in range(len(m.labels_test)):
		f.write(str(m.labels_test[i][0]) +  '\t ' + str(m.labels_test[i][1]) + '\n')
	f.close()
	index +=1

		# ------------------- Write Average results to a file -------------------
	fd.write('\n\nAVERAGE RESULTS')
	fd.write('\nPrecision :' + str(np.mean(m.precision)) + '\tstd : ' + str(np.std(m.precision)))
	fd.write('\nRecall :' + str(np.mean(m.recall)) + '\tstd : ' + str(np.std(m.recall)))
	fd.write('\nF-measure :' + str(np.mean(m.hf)) + '\tstd : ' + str(np.std(m.hf)))
	fd.write('\n\n')

	for i in range(len(m.precision_level[-1])):
		fd.write('\nPrecision level ' + str(i+1) + ' \t ' + str(np.mean(m.precision_level,axis=0)[i]) + ' \tstd: ' +str(np.std(m.precision_level,axis=0)[i]))
		fd.write('\nRecall level '+ str(i+1) + ' \t ' + str(np.mean(m.recall_level,axis=0)[i]) + ' \tstd: ' + str(np.std(m.recall_level,axis=0)[i]))
		fd.write('\nF-measure level: '+ str(i+1) +  ' \t ' + str(np.mean(m.hf_level,axis=0)[i]) + ' \tstd: ' + str(np.std(m.hf_level,axis=0)[i]))
		fd.write('\n------------------------------------------------------------------------------------------------------')  

	fd.close()


if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-f", "--filename", dest="filename", help="Name of the training file.")
	parser.add_option("-n", "--node_file", dest="node_file", help="Path to node filelist.", default="node.txt")
	parser.add_option("-c", "--c_value", dest="c_value", help="c parameter for SVM")
	parser.add_option("-g", "--gamma_value", dest="gamma_value", help="gamma parameter for SVM")

		
	# Hierarchical classification algorithm can be either:
	# 		non-Leaf Local Classifier per Parent Node (nLCPN)
	# 		Local Classifier per Parent Node and Branch (LCPNB)

	parser.add_option("-a", "--algorithm", dest="algorithm", help="Hierarchical classification algorithm LCPNB or nLLCPN.", default='lcpnb')

	(options, args) = parser.parse_args()
    #nodes_filepath = sys.argv[1]
	dataset_filepath = "./data/"
	node_filepath = "./nodes/"

	h = hie.hierarchy(node_filepath + options.node_file)

	with open(dataset_filepath + options.filename , "r") as csvfile:
		data = pd.read_csv(csvfile, low_memory=False)


	X4 = data.iloc[:, 0:(pow(4,2) + pow(4,3) + pow(4,4))]
	Y = data.iloc[:,-1]

	main(options.algorithm, X4, Y, options.c_value, options.gamma_value)
	print("---------------------------------------------Ending Training---------------------------------------------")

