#MIT Open License
#Manisha

import pickle
import sys
import os
import subprocess
import shutil
from optparse import OptionParser
from shutil import copy2

def feature_generation(curr_dir1):
	#copy list.txt to features/ and  features/kanalyze-2.0.0/code
	feature_destpath = curr_dir1 + "/features/" 
	kanalyzer_destpath = feature_destpath + "kanalyze-2.0.0/code/"
	kanalyzer_input_destpath = feature_destpath + "kanalyze-2.0.0/input_data/"
	kanalyzer_output_destpath = feature_destpath + "kanalyze-2.0.0/output_data/"


	mer2_dir = kanalyzer_output_destpath + '2mer/'
	mer3_dir = kanalyzer_output_destpath + '3mer/'
	mer4_dir = kanalyzer_output_destpath + '4mer/'



	if os.path.isdir(mer2_dir):
		subprocess.run(['rm','-R',kanalyzer_output_destpath + '2mer'])
		os.mkdir(mer2_dir)
	else:
		os.mkdir(mer2_dir)

	if os.path.isdir(mer3_dir):
		subprocess.run(['rm','-R',kanalyzer_output_destpath + '3mer'])
		os.mkdir(mer3_dir)
	else:
		os.mkdir(mer3_dir)

	if os.path.isdir(mer4_dir):
		subprocess.run(['rm','-R',kanalyzer_output_destpath + '4mer'])
		os.mkdir(mer4_dir)
	else:
		os.mkdir(mer4_dir)

	#chmod 775 runKanalyzer_generate_all_features and run this script
	curr_dir = os.getcwd()
	kanalyzer_dir = os.chdir(kanalyzer_destpath)
	curr_dir = os.getcwd() + "/"


	subprocess.run(['chmod', '775', 'runKanalyzer_generate_all_features'])
	subprocess.run(['./runKanalyzer_generate_all_features'])

	change_dir = os.chdir(feature_destpath)
	
	
	subprocess.run(['javac','KmersFeaturesCollector.java'])
	subprocess.run(['javac','BufferReaderAndWriter.java'])
	subprocess.run(['java', 'KmersFeaturesCollector'])

	
	curr_dir2 = os.getcwd()
	change_dir = os.chdir(curr_dir1)
	data_dir = 'data/'
	shutil.copy2(curr_dir2+'/feature_file.csv', data_dir+'feature_file.csv')
	change_dir = os.chdir(feature_destpath)
	subprocess.run(['rm', 'feature_file.csv'])
	change_dir = os.chdir(curr_dir1)

	

def get_data(fasta_file):
	curr_dir1 = os.getcwd()
	data_filepath = curr_dir1 + "/data/"
	feature_destpath = curr_dir1 + "/features/" 
	kanalyzer_destpath = feature_destpath + "kanalyze-2.0.0/code/"
	kanalyzer_input_destpath = feature_destpath + "kanalyze-2.0.0/input_data/"

	if os.path.isdir(kanalyzer_input_destpath):
		subprocess.run(['rm','-R',kanalyzer_input_destpath])
		os.mkdir(kanalyzer_input_destpath)
	else:
		os.mkdir(kanalyzer_input_destpath)

	sequence = ""
	with open(data_filepath+ fasta_file, 'rt') as fp: 
		content = fp.read()
		data = content.split(">")
		#print(data)
		i=0
		for line in data:
			meta = line.strip("\n")
			if meta != "":
				of = open(kanalyzer_input_destpath + "seq" + str(i+1)+".fasta" ,"w")
				of.write(">" + meta)
				i=i+1
				of.close()
	fp.close()
	curr_dir2 = os.getcwd() + "/features/kanalyze-2.0.0/input_data/"
	change_dir = os.chdir(curr_dir2)
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	with open("list.txt", "w") as ff:
		for f in files:
			#print(f)
			ff.write(f)
			ff.write('\n')
	ff.close()
	shutil.copy2('./list.txt', feature_destpath+"list.txt")
	shutil.copy2('./list.txt', kanalyzer_destpath+"list.txt")
	subprocess.run(['rm', 'list.txt'])


def main():

	
	curr_dir1 = os.getcwd()
	parser = OptionParser()

	parser.add_option("-f", "--filename", dest="filename", help="Name of the training file.")
	#parser.add_option("-m", "--modelname", dest="modelname", help="Model name")
	(options, args) = parser.parse_args()
	fasta_file = options.filename
	get_data(fasta_file)


	#if we want to provide sequence in the command line, uncomment following
	# te_id = sys.argv[1]
	# fasta = sys.argv[2]
	# fasta_filepath = "fasta"
	# if not os.path.isdir(fasta_filepath):
	# 		os.mkdir(fasta_filepath)
	# fasta_filename = str(te_id) + ".fasta"

	# with open(os.path.join(fasta_filepath, fasta_filename), "w") as fd:
	# 	fd.write(">" + str(te_id) + "\n")
	# 	fd.write(fasta)
	# fd.close()

	# with open("list.txt", "w") as f:
	# 	f.write(str(te_id)+ ".fasta")
	# f.close()

	feature_generation(curr_dir1)
	#subprocess.run(['python', 'evaluate.py','-f','feature_file.csv','-n','node.txt', 'm', ''])
	


if __name__ == '__main__':
	main()