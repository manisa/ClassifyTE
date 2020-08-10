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
import hierarchy as hie
import model as mo
import classification as cl

def main(algorithm, X, Y, kmer):
	#------------------------ create file to store overall results --------------------------
	output_filepath = 'results'
	if not os.path.isdir(output_filepath):
		os.mkdir(output_filepath)
	output_filename = 'result_' + str(kmer) + '.txt'

	fd = open(os.path.join(output_filepath, output_filename), 'w')


	# ------------------------- Generate ML Models and test them using train_test_split . -----------------------------
	
	#data = pd.concat([X, Y], axis=1)
	
	index = 1
	
	print("Iteration", str(index))
	
	#X_train, y_train = X.iloc[train_idx], Y.iloc[train_idx]
	#X_test, y_test = X.iloc[test_idx], Y.iloc[test_idx]

	#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20, stratify=Y, random_state=42)

	train_data = pd.concat([X, Y], axis=1)
	test_data = pd.concat([X, Y], axis=1)

	parent_classifiers = {}
	train_data_parent = pd.DataFrame.copy(train_data)
	train_label = pd.DataFrame(train_data['classification'])
	train_data = pd.DataFrame(train_data.drop('classification',axis=1))

	dataInnerNode = h.getDataFromInnerNodes(train_data_parent)

	test_label = pd.DataFrame(test_data['classification'])
	test_data = pd.DataFrame(test_data.drop('classification', axis=1))

	m = mo.model(h, algorithm)
	parent_classifiers1 = m.generate_models(dataInnerNode, kmer, index)

	input_filepath = 'Models/'
	pkl_filename = "pickle_model_" + str(index) + "_" +  str(kmer) + ".pkl"
	
	with open(input_filepath + pkl_filename, 'rb') as fb:
		parent_classifiers = pickle.load(fb)

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
    
	
	
	fold_output_filename = "fold" + str(index) + "_labels_test_" +  str(kmer) + ".txt"
	f = open(os.path.join(output_filepath, fold_output_filename) ,'w')
	f.write('true \t predicted\n')
	for i in range(len(m.labels_test)):
		f.write(str(m.labels_test[i][0]) +  '\t ' + str(m.labels_test[i][1]) + '\n')
	f.close()
	

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
	parser.add_option("-n", "--nodes_filepath", dest="nodes_filepath", help="Path to node filelist.")
	
	# Hierarchical classification algorithm can be either:
	# 		non-Leaf Local Classifier per Parent Node (nLCPN)
	# 		Local Classifier per Parent Node and Branch (LCPNB)

	parser.add_option("-a", "--algorithm", dest="algorithm", help="Hierarchical classification algorithm LCPNB or nLLCPN.", default='lcpnb')

	(options, args) = parser.parse_args()
    #nodes_filepath = sys.argv[1]
	dataset_filepath = "./data/"

	h = hie.hierarchy(options.nodes_filepath)

	with open(dataset_filepath + options.filename , "r") as csvfile:
		data = pd.read_csv(csvfile, low_memory=False)

#	X1 = data.iloc[:, 0:pow(4,1)]
#	X2 = data.iloc[:, 0:(pow(4,1) + pow(4,2))]
#	X3 = data.iloc[:, 0:(pow(4,1) + pow(4,2) + pow(4,3))]
	X4 = data.iloc[:, 0:(pow(4,2) + pow(4,3) + pow(4,4))]
#	X5 = data.iloc[:, 0:(pow(4,1) + pow(4,2) + pow(4,3) + pow(4,4) + pow(4,5))]
#	X6 = data.iloc[:, 0:(pow(4,1) + pow(4,2) + pow(4,3) + pow(4,4) + pow(4,5) + pow(4,6))]

	Y = data.iloc[:,-1]

	#X_train1, X_test1, Y_train1, Y_test1 = train_test_split(X1, Y, test_size=0.20, stratify=Y, random_state=42)
	# X_train2, X_test2, Y_train2, Y_test2 = train_test_split(X2, Y, test_size=0.20, stratify=Y, random_state=42)
	# X_train3, X_test3, Y_train3, Y_test3 = train_test_split(X3, Y, test_size=0.20, stratify=Y, random_state=42)
	# X_train4, X_test4, Y_train4, Y_test4 = train_test_split(X4, Y, test_size=0.20, stratify=Y, random_state=42)
	# X_train5, X_test5, Y_train5, Y_test5 = train_test_split(X5, Y, test_size=0.20, stratify=Y, random_state=42)
	# X_train6, X_test6, Y_train6, Y_test6 = train_test_split(X6, Y, test_size=0.20, stratify=Y, random_state=42)

	# train_data1 = pd.concat([X_train1, Y_train1], axis=1)
	# test_data1 = pd.concat([X_test1, Y_test1], axis=1)
	# train_data2 = pd.concat([X_train2, Y_train2], axis=1)
	# test_data2 = pd.concat([X_test2, Y_test2], axis=1)
	# train_data3 = pd.concat([X_train3, Y_train3], axis=1)
	# test_data3 = pd.concat([X_test3, Y_test3], axis=1)
	# train_data4 = pd.concat([X_train4, Y_train4], axis=1)
	# test_data4 = pd.concat([X_test4, Y_test4], axis=1)
	# train_data5 = pd.concat([X_train5, Y_train5], axis=1)
	# test_data5 = pd.concat([X_test5, Y_test5], axis=1)
	# train_data6 = pd.concat([X_train6, Y_train6], axis=1)
	# test_data6 = pd.concat([X_test6, Y_test6], axis=1)



	main(options.algorithm, X4, Y, 1)
	print("---------------------------------------------Ending Training k=1---------------------------------------------")

	# main(options.algorithm, X2, Y, 2)
	# print("---------------------------------------------Ending Training k=1,2---------------------------------------------")
	
	# main(options.algorithm, X3, Y, 3)
	# print("---------------------------------------------Ending Training k=1,2,3---------------------------------------------")

	# main(options.algorithm, X4, Y, 4)
	# print("---------------------------------------------Ending Training k=1,2,3,4---------------------------------------------")

	# main(options.algorithm, X5, Y, 5)
	# print("---------------------------------------------Ending Training k=1,2,3,4,5---------------------------------------------")

	# main(options.algorithm, X6, Y, 6)
	# print("---------------------------------------------Ending Training k=1,2,3,4,5,6---------------------------------------------")
 #    # algorithm = str(input("Enter the classification strategy.\nEither 'lcpnb' or 'nllcpn'. "))
    # if algorithm == 'lcpnb':
    #     main(algorithm)
    # elif algorithm == 'nllcpn':
    #     main(algorithm)
    # else:
    #     print('Wrong classification strategy. Enter again!')


