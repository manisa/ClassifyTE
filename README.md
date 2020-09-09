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
- [Acknowledgements](#achknowledgement)
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

- Create and activate the virtual environment with python dependendencies
```
conda env create -f environment.yml
conda activate ClassifyTE_env
```


## Download Models
- Go to [this link](https://drive.google.com/drive/folders/1JqbE1bl9k54hMiS4ffCWfYZjcDiFU68b?usp=sharing)
- Click on ClassifyTE_Models. This will automatically download models built with TE datasets.
- Unzip and copy the folder *Models* into root folder *ClassifyTE".
- Your directory structure should look like this:

```
ClassifyTE/
	Models/
		Mixed.pkl
		Repbase.pkl
		MIPS.pkl

```

## Download datasets
- Go to [this link](https://drive.google.com/drive/folders/1JqbE1bl9k54hMiS4ffCWfYZjcDiFU68b?usp=sharing)
- Click on ClassifyTE_Datasets. This will automatically download models built with TE mixed dataset.
- Unzip and copy the folder *Models* into root folder *ClassifyTE".
- Your directory structure should look like this:

```
ClassifyTE/
	Data/
		mips_features_TE_upto_6mer.csv
		repbase_features_TE_upto_6mer.csv
		mips+repbase_features_TE_upto_6mer.csv
		

```
## Demo

```

```

## Training
- To replicate the training procedure, follow following command line
```
  python train.py -f csv_file_name -n txt_node_file -c SVM_cost_parameter -g SVM_gamma_parameter
```
- Training example would look like as below:
```
python train.py -f repbase_features_TE_upto_6mer.csv -n node_repbase.txt -c 128.0 -g 0.0078125
```

## Authors
Manisha Panta, Avdesh Mishra, Md Tamjidul Hoque, joel Atallah
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## References
-[1] Nakano, F.K., et al. Top-down Strategies for Hierarchical Classification of Tranposable Elelments with Neural Networks. In, IEEE. 2017.

