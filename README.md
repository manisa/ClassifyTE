# ClassifyTE: Stacking-based Machine Learning Framework for Hierarchical Classification of transposable 

Manisha Panta, Avdesh Mishra, Md Tamjidul Hoque, and Joel Atallah

- [Paper](https://arxiv.org/abs/1907.01674)

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
- Go to [this link](https://cs.uno.edu/~tamjid/Software.html)
- Click on ClassifyTE_Models. This will automatically download models built with TE datasets.
- Unzip and copy the folder *Models* into root folder *ClassifyTE".
- Your directory structure should look like this:

```
ClassifyTE/
	Models/
		ClassifyTE.pkl
		Repbase.pkl
		MIPS.pkl

```

## Download datasets
- Go to [this link](https://cs.uno.edu/~tamjid/Software.html)
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
- 
## Demo



```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


