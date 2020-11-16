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
- Click on **ClassifyTE_Models.zip**. This will automatically download models built with TE datasets.
- Unzip and copy all the models from "ClassifyTE_Models" directory into the folder **model** inside the root folder **ClassifyTE**.
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
- Click on **ClassifyTE_Datasets.zip**. This will automatically download the datasets used to generate models.
- Unzip and copy all the datasets from **ClassifyTE_Datasets** directory into the folder **data** inside the root folder **ClassifyTE**.
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
- Firstly, Run following python command from the root directory to generate feature file.
```
python generate_feature_file.py -f demo.fasta
```

#### *Parameters*
For **generate_feature_file.py**, the user has to provide two parameters:
- -f for fasta filename from  **data** directory.
- -o for resulting feature file name with **.csv** extension [**Optional**]  [By default the feature filename is **feature_file.csv**.]

- Then run following python command from the root directory to get the prediction on new TE sequences. Prior following command, please make sure that all the model files have already been added to **models** directory. 

```
python evaluate.py -f feature_file.csv -n node.txt -m ClassifyTE_combined.pkl
```
#### *Parameters*
For **evaluate.py**, the user has to provide following parameters:
- -f for feature file name which is by default *feature_file.csv* unless user have provided a feature filename in earlier step.
- -n for node filename which is by default *node.txt*. Node file consists of numerical representation of taxonomy of the dataset. Please check nodes folder for other node files for each dataset.
- -m for model filename which has **.pkl** as file extension. All the model files must have been added in **models** directory.

- Finally, check **predicted_result.csv** file inside **output** folder for predicted label of the TE sequence/s.

## Deployment
To run the program on **new** TE sequence:
- Place your fasta file (with single or multiple fasta sequences) inside **data** folder.
- Your directory structure should look like this

```
ClassifyTE/
	data/
		[your_fasta_file]
```
- Firstly, Run following python command from the root directory to generate feature file.
```
python generate_feature_file.py -f your_fasta_file_name -o your_feature_file_name
```

#### *Parameters*
For **generate_feature_file.py**, the user has to provide two parameters:
- -f for fasta filename from  **data** directory.
- -o for resulting feature file name with **.csv** extension [**Optional**]  [By default the feature filename is **feature_file.csv**.]

- Then run following python command from the root directory to get the prediction on new TE sequences. Prior following command, please make sure that all the model files have already been added to **models** directory. 

```
python evaluate.py -f your_feature_file_name -n node.txt -m ClassifyTE_combined.pkl
```
#### *Parameters*
For **evaluate.py**, the user has to provide following parameters:
- -f for feature file name which is by default *feature_file.csv* unless user have provided a feature filename in earlier step.
- -n for node filename which is by default *node.txt*. Node file consists of numerical representation of taxonomy of the dataset. Each node file is associated with the respective models trained on respective datasets. Please check [below](#nodes) section for details.
- -m for model filename which has **.pkl** as file extension. All the model files must have been added in **models** directory.

- Finally, check **predicted_result.csv** file inside **output** folder for predicted label of the TE sequence/s.

## Training
- To replicate the training procedure, follow following command line
```
python train.py -f csv_file_name -n txt_node_file -c SVM_cost_parameter -g SVM_gamma_parameter
```

#### *Parameters*
For **train.py**, the user has to provide following parameters:
- -f for feature file name.
- -n for node filename. Node file consists of numerical representation of taxonomy of the dataset.
- -c for cost parameter of SVM with RBF kernel
- -g for gamma parameter of SVM with RBF kernel

- We have optimized cost and gamma parameters of SVM with RBF kernel for all three datasets. The cost and gamma parameters for training each datasets would be different. You will have to pass the hyper-parameters accordingly. 
```
For PGSB dataset : C=32, gamma=0.03125
For REPBASE dataset : C=128.0, gamma=0.0078125
For mixed dataset : C=512.0, gamma=0.0078125
```

##### nodes 
- Under **node** directory you will find three files. These files consists of all the nodes in each of the corresponding datasets. 
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
[1] Nakano, F.K., et al. Top-down Strategies for Hierarchical Classification of Tranposable Elements with Neural Networks. In, IEEE. 2017.

