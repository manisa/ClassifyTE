# ClassifyTE: Stacking-based Machine Learning Framework for Hierarchical Classification of transposable 

- [Paper](https://arxiv.org/abs/1907.01674)
- The basic framework has been adapted from the state-of-the-art method [1].

### Table of Content
- [Setup](#getting-started)
	- [Download and install code](#download-and-install-code)
	- [Download Models](#download-models)
	- [Demo](#demo)
- [Training](#training)
	- [Download Datasets](#download-datasets)
- [References](#references)


# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites

You would need to install the following software before replicating this framework in your local or server machine.

```
Java JDK
Python version 3.5+
Aanaconda version 3+
```

## Download and install code
- Retrieve the code
```sh
git clone https://github.com/manisa/ClassifyTE.git
cd ClassifyTE
```

- Create and activate the virtual environment with python dependendencies. 
```
conda env create -f environment.yml python==3.7
conda activate ClassifyTE_env
```


## Download Models
- Go to [this link](https://drive.google.com/file/d/1fwlAJOXQneXu4OMNVQhT17lpfmvvyYuU/view?usp=sharing).
- Click on *ClassifyTE_Models.zip*. This will automatically download models built with TE datasets.
- Unzip and copy all the models from "ClassifyTE_Models" directory into the folder *model* inside the root folder *ClassifyTE*.
- Your directory structure should look like this:

```
ClassifyTE/
	models/
		ClassifyTE_combined.pkl
		ClassifyTE_repbase.pkl
		ClassifyTE_mips.pkl
```

## Download datasets
- Go to [this link](https://drive.google.com/file/d/1vZKPjug1LsH75a7JdKKMi10ECTjUIwAm/view?usp=sharing).
- Click on *ClassifyTE_Datasets.zip*. This will automatically download the datasets used to generate models.
- Unzip and copy all the datasets from *ClassifyTE_Datasets* directory into the folder *data* inside the root folder *ClassifyTE*.
- Your directory structure should look like this:

```
ClassifyTE/
	data/
		mips_features_TE_upto_6mer.csv
		repbase_features_TE_upto_6mer.csv
		mips+repbase_features_TE_upto_6mer.csv
```
## Demo
To run the program on test TE sequence:
- Your directory structure should look like this with the demo.fasta file.

```
ClassifyTE/
	data/
		demo.fasta
```
- Then run following python command from the root directory.
```
python generate_feature_file.py -f demo.fasta
python evaluate.py -f feature_file.csv -n node.txt -m ClassifyTE_combined.pkl
```
- check *predicted_result.csv* file inside *output* folder for prediction 

## Deployment
To run the program on *new* TE sequence:
- Create a folder named *data* inside *ClassifyTE*.
- Place your fasta file (with single or multiple fasta sequences) inside *data* folder.
- Your directory structure should look like this

```
ClassifyTE/
	data/
		[your_fasta_file]
```
- Then run following python command
```
python generate_feature_file.py -f your_fasta_file
python evaluate.py -f feature_file.csv -n node.txt -m your_choice_of_model
```

## Training
- To replicate the training procedure, follow following command line
```
python train.py -f csv_file_name -n txt_node_file -c SVM_cost_parameter -g SVM_gamma_parameter
```
- We have optimized cost and gamma parameters of SVM with RBF kernel for all three datasets. The cost and gamma parameters for training each datasets would be different. You will have to pass the hyper-parameters accordingly. 
```
For PGSB dataset : C=32, gamma=0.03125
For REPBASE dataset : C=128.0, gamma=0.0078125
For mixed dataset : C=512.0, gamma=0.0078125
```
- Under *node* directory you will find three files. These files consists of all the nodes in each of the corresponding datasets. 
	1.	node_pgsb.txt 
	2.	node_repbase.txt
	3.	node.txt

- If you would like to train the model on your machine, the training example would look like as below:
```
python train.py -f repbase_features_TE_upto_6mer.csv -n node_repbase.txt -c 128.0 -g 0.0078125
```

## Authors
Manisha Panta, Avdesh Mishra, Md Tamjidul Hoque, Joel Atallah
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## References
[1] Nakano, F.K., et al. Top-down Strategies for Hierarchical Classification of Tranposable Elelments with Neural Networks. In, IEEE. 2017.

