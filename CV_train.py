import numpy as np
import pandas as pd
import sys
import os
import math
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

def main(algorithm, X, Y):
	#------------------------ create file to store overall results --------------------------
	output_filepath = 'CV_Results'
	if not os.path.isdir(output_filepath):
		os.mkdir(output_filepath)
	output_filename = 'CV_Results' +'.txt'

	fd = open(os.path.join(output_filepath, output_filename), 'w')


	# ------------------------- Generate ML Models and test them using 10-Fold CV. -----------------------------
	
	#------------------------- create gid of hyper paramenters ----------------------------
	c_range = np.linspace(-5,15,num=5)
	C_range = [math.pow(2,i) for i in c_range]
	g_range = np.linspace(-15,5,num=5)
	gamma_range = [math.pow(2,j) for j in g_range]


	#------------------------ create file to store overall results --------------------------
	output_filepath = 'results'
	if not os.path.isdir(output_filepath):
		os.mkdir(output_filepath)


	gridsearch_filename = 'result' + '_gridsearch' + '.txt'
	gridsearch_results = open(os.path.join(output_filepath, gridsearch_filename), 'w')

	cv = StratifiedKFold(n_splits=3)
	#data = pd.concat([X, Y], axis=1)
	index = 1
	for cost in C_range:
		for gamma in gamma_range:
			for train_idx, test_idx, in cv.split(X, Y):
				print("Iteration", str(index))
				
				X_train, y_train = X.iloc[train_idx], Y.iloc[train_idx]
				X_test, y_test = X.iloc[test_idx], Y.iloc[test_idx]

				train_data = pd.concat([X_train, y_train], axis=1)
				test_data = pd.concat([X_test, y_test], axis=1)

				parent_classifiers = {}
				train_data_parent = pd.DataFrame.copy(train_data)
				train_label = pd.DataFrame(train_data['classification'])
				train_data = pd.DataFrame(train_data.drop('classification',axis=1))

				dataInnerNode = h.getDataFromInnerNodes(train_data_parent)

				test_label = pd.DataFrame(test_data['classification'])
				test_data = pd.DataFrame(test_data.drop('classification', axis=1))

				m = mo.model(h, algorithm)
				parent_classifiers = m.generate_models(dataInnerNode, index, cost, gamma)

				# Save models
				#input_filepath = 'Models/'
				#pkl_filename = "pickle_model_" + str(neurons) + str(index) + ".pkl"
				
				#with open(input_filepath + pkl_filename, 'rb') as fb:
				#	parent_classifiers = pickle.load(fb)

				m.test_model(test_data, test_label, parent_classifiers)


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
			    
				
		    	
				fold_output_filename = "fold" + str(index) + "_labels_test_" +  str(neurons) + ".txt"
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

			fd.flush()
			fd.close()

			gridsearch_results.write("cost = "+str(cost)+"\tgamma = "+str(gamma)+"\tmean test precision = "+str(np.mean(m.precision))+"\tmean test recall = "+str(np.mean(m.recall))+"\tmean test F-measure"+str(np.mean(m.hf))+'\n')
			gridsearch_results.flush()
	gridsearch_results.close()


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
	dataset_filepath = "./data/"
	node_filepath = "./nodes/"

	h = hie.hierarchy(node_filepath + options.node_file)

	with open(dataset_filepath + options.filename , "r") as csvfile:
		data = pd.read_csv(csvfile, low_memory=False)

	X = data.iloc[:,0:-1]
	Y = data.iloc[:,-1]

	main(options.algorithm, X, Y)
	print("---------------------------------------------Ending Training for 55 neurons---------------------------------------------")