import os
import numpy as np
import pandas as pd
import sys
import pickle
from sklearn import svm
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from HierStack import classification as cl
# from stackingClassifier import *


class model:
    def __init__(self, h, algo):
        self.algorithm = algo
        self.h = h
        self.precision = []
        self.recall = []
        self.hf = []
        self.precision_level = []
        self.recall_level = self.hf_level = []
        self.labels_test = []

    def generate_models(self, dataInnerNode, n, cost, gammas):
        output_filepath = 'models'
        if not os.path.isdir(output_filepath):
            os.mkdir(output_filepath)
        parent_models = "parent_models" + "_" + str(n) + ".dat"

        parent_classifiers = {}
        for node in dataInnerNode:
            base_classifiers = []
            meta_classifier = []
            
            node_dataset = dataInnerNode[node]  
            node_data = node_dataset.drop('classification',axis=1)
            node_data = pd.DataFrame(node_data)

            
            node_label = node_dataset['classification']
            node_label = pd.DataFrame(node_label.iloc[node_data.index.values])      
            
            param = {'C' : cost, 'gamma' : gammas}

            clf = Pipeline([('scaler', preprocessing.StandardScaler()),('SVM_RBF', SVC(C=cost, gamma=gammas, kernel='rbf',class_weight='balanced',probability=True, random_state=42))])
            
            #clf= svm.SVC(C=cost, kernel='rbf', gamma=gamma, probability=True)

            X = node_data.values
            y = node_label.values.ravel()

            if len(np.unique(node_label.values))==1:
                parent_classifiers[node] = str(np.unique(node_label.values)[0])
            else:
                parent_classifiers[node] = clf.fit(X,y)
		
        #---------------------- Save Models to files---------------------------

        with open(os.path.join(output_filepath, parent_models), "wb") as fm:
            pickle.dump(parent_classifiers, fm)
        return parent_classifiers

    def test_model(self, test_data, test_label, parent_classifiers):
        pi_ti = 0
        pi = 0
        ti = 0
        pi_ti_level = np.zeros(self.h.getHeight())
        pi_level = np.zeros(self.h.getHeight())
        ti_level = np.zeros(self.h.getHeight())
        
        for i in range(len(test_data)):
            c = cl.classification(test_label.iloc[i]['classification'], self.h,self.algorithm )
            c.classify(test_data.iloc[i].values.reshape(1,-1),parent_classifiers)
            
            pi_ti+=c.getPiTi()
            pi+=c.getPi()
            ti+=c.getTi()

            self.labels_test.append((c.true,c.predicted))
            
            pi_ti_level+=c.getPiTiPerLevel()
            pi_level+=c.getPiPerLevel()
            ti_level+=c.getTiPerLevel()
        
        #--------------------------------------Compute hierarchical classficaition metrics------------------------------------
        self.precision.append(pi_ti/pi)
        self.recall.append(pi_ti/ti)
        self.hf.append(2  * self.precision[-1] * self.recall[-1]/(self.precision[-1] + self.recall[-1]))

        self.precision_level.append(pi_ti_level/pi_level)
        self.recall_level.append(pi_ti_level/ti_level)
        self.hf_level.append(2  * np.multiply(self.precision_level[-1],self.recall_level[-1])/(self.precision_level[-1] + self.recall_level[-1]))
