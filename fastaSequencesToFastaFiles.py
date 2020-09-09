#! /usr/bin/env python

import os
#input_path = "/home/manisha/new_TE_Classification_Project/TE/data/all_Fasta_Files/Repbase"
output_path = "/home/mpanta1/Research/TE_BioinformaticsReview/ClassifyTE/fasta/"
output_path1 = "/home/mpanta1/Research/TE_BioinformaticsReview/tools_comparison/Repbase/"

sequence = ""
with open('/home/mpanta1/Research/TE_BioinformaticsReview/tools_comparison/ltr_classifier_MIPS.fasta', 'rt') as fp: 
	content = fp.read()
	data = content.split(">")
	#print(data)
	i=0
	for line in data:
		meta = line
		of = open(output_path + "fasta_file" + str(i)+".fasta" ,"w")
		of.write(">" + meta)
		i=i+1
fp.close()
of.close()

