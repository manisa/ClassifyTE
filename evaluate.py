import numpy as np
import pandas as pd
import sys
import os
import csv
import time
import argparse
from optparse import OptionParser
from sklearn.linear_model import LogisticRegression



import pickle
from HierStack import hierarchy as hie
from HierStack import model as mo
from HierStack import lcpnb as cl
from HierStack.stackingClassifier import *

def getSequenceName(curr_dir):
	input_files_dir = curr_dir+"/features/kanalyze-2.0.0/input_data/"
	_, _, files = next(os.walk(input_files_dir))
	files = sorted(files)
	seqIDs = []
	for file in files:
		f = open(input_files_dir + file,"r")
		header = f.readline()
		head = header.split(">")
		ID = head[1]
		seqIDs.append(ID)
	return seqIDs

def getLabel(content, predicted):
	if predicted in content:
		label = content[predicted]
		label = label.strip("\n")
		return label


def getCodeLabel(lines):
	content = dict()
	code = []
	label = []	
	for line in lines:
		data = line.split(",")
		code.append(data[0])
		label.append(data[1])
	content = dict(zip(code,label))
	return content


def main(algorithm, data, modelname):
	# ------------------------- Generate hierarcical classification for the sequence-----------------------------
	model_filepath = "models/"
	output_filepath = "output/"
	pkl_filename = modelname

	test_data = data.iloc[:, 0:(pow(4,2) + pow(4,3) + pow(4,4))]
	test_label = data.iloc[:,-1]

	parent_classifiers = {}

	with open(model_filepath + pkl_filename, 'rb') as fb:
		parent_classifiers = pickle.load(fb)

	print("---------------------------------------------Evaluation Started---------------------------------------------\n")
	m = mo.model(h, algorithm)

	labels_test = m.evaluate_model(test_data, parent_classifiers)

	return labels_test



if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-f", "--filename", dest="filename", help="Name of the training file.")
	parser.add_option("-n", "--node_file", dest="node_file", help="Path to node filelist.", default="node.txt")
	parser.add_option("-m", "--modelname", dest="modelname", help="Model name")
	
	# Hierarchical classification algorithm can be either:
	# 		non-Leaf Local Classifier per Parent Node (nLCPN)
	# 		Local Classifier per Parent Node and Branch (LCPNB)

	parser.add_option("-a", "--algorithm", dest="algorithm", help="Hierarchical classification algorithm LCPNB or nLLCPN.", default='lcpnb')

	(options, args) = parser.parse_args()

	curr_dir1 = os.getcwd()
	dataset_filepath = curr_dir1 + "/data/"
	node_filepath = curr_dir1 + "/nodes/"
	seq_names = getSequenceName(curr_dir1)
	
	h = hie.hierarchy(node_filepath + options.node_file)
	start_time = time.time()

	with open(dataset_filepath + options.filename , "r") as csvfile:
		data = pd.read_csv(csvfile, low_memory=False)

	with open("./nodes/tree.txt", "r") as f:
		lines = f.readlines()
		content = getCodeLabel(lines)
	f.close()
	

	hier_label = {}
	hier_label = main(options.algorithm, data, options.modelname)

	output_filepath = "output/"
	output_filename = "predicted_result.txt"
	f = open(os.path.join(output_filepath, output_filename) ,'w')
	f.write('--------------------------------Predictions--------------------------------\n')
	f.write('\n')
	
	
	count = 0
	for k in hier_label:
		name = str(seq_names[count])
		print("Prediction for TE sequence of ID: {}".format(name))
		f.write("Prediction for TE sequence of ID: {}".format(name))
		j = 1
		predicted_labels = []
		for i in k:
			label = getLabel(content,str(i))	
			predicted_labels.append(str(label))
			print("Predicted level {} : {}".format(str(i), str(label)))
			f.write("Predicted level {} : {}".format(str(i), str(label)))
			f.write("\n")
			#f.write(str(label) + ',')
			j = j +1
		# wr = csv.writer(f, dialect='excel')
		# f.write(str("TE Sequence ID: " + name)
		# f.write('Level 1,' + 'Level 2,' + 'Level 3,' + 'Level 4' + '\n' )
		# wr.writerow(predicted_labels)
		f.write("Final label of TE sequence is {}".format(label))
		f.write('\n\n')
		f.write('###############################################################')
		f.write('\n\n')
		print('\n')
		print('###############################################################')
		print('\n')
		count +=1
	f.close()
	elapsed_time = time.time() - start_time
	print("\nTotal time elapsed in seconds\t", elapsed_time)
	

