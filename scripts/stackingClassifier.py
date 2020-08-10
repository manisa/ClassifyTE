#testing leave-one-out CV ie Jack Knife sampling technique to compute biasness

from sklearn.base import *
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.model_selection import cross_val_predict,LeaveOneOut

from copy import deepcopy


def get_probabilities(model, X):
	pred = model.predict_proba(X)	
	return pred

def get_predictions(model, X):
	pred = model.predict(X)	
	return pred

def get_classes(model, X):
	classes = model.classes_
	return classes


class StackingClassifier:
	base_models = []
	meta_classifier = []
	copy_base_models = []
	copy_meta_model = None


	def __init__(self, classifiers = [], meta_classifier = []):
		self.base_models = classifiers
		self.meta_classifier = meta_classifier
		self.classes_ = []
		self.copy_base_models = []
		self.copy_meta_model

	
	def fit_base_models(self, X, y, loc):
		cv_probabilities = []
		for i, clf in enumerate(self.base_models):
			print('---------------------------fitting base model-------------------------')
			clf_prediction = cross_val_predict(clf, X, y, cv=10, method='predict_proba', n_jobs=-1)
			np.savetxt(loc + "Train_probab_" + str(i) + ".csv", clf_prediction, delimiter=",")
			cv_probabilities.append(clf_prediction)
			clf.fit(X, y)
			f1 = open(loc + 'model_' + str(i), 'wb')
			pickle.dump(clf,f1)
			self.copy_base_models.append(deepcopy(clf))
		cv_probabilities = np.hstack(cv_probabilities)
		np.savetxt(loc + "Final_Prediction" + ".csv", cv_probabilities, delimiter=",")
		return cv_probabilities

			

	def transform_base_models(self, X):
		probabilities = []
		for i, clf in enumerate(self.copy_base_models):
			pred_classifier = []
			pred_classifier = get_probabilities(clf, X)
			probabilities.append(pred_classifier)
		probabilities = np.hstack(probabilities)
		return probabilities



	def create_x_blending(self, X_meta_probabilities, X):
		#probabilities = self.transform_base_models(X)
		X_blending = np.hstack((X, X_meta_probabilities))
		return X_blending
		#return probabilities


	def create_directories(self, indexing, noding):
		output_filepath = indexing + "/" + noding
		if not os.path.isdir(output_filepath):
		    os.makedirs(output_filepath)
		

	def fit(self, X, y,node,index):


		indexing = "models_fold_" + str(index)
		noding = indexing + "_" + str(node)
		
		self.create_directories(indexing, noding)
		loc = os.getcwd() + "/" + indexing + "/" + noding + "/"		

		X_meta_probabilities = self.fit_base_models(X, y,loc)
		X = self.create_x_blending(X_meta_probabilities, X)
		#print(X)	
		clf = self.meta_classifier
		clf.fit(X,y)
		self.copy_meta_model = deepcopy(clf)
		self.classes_ = np.unique(y)	
		return self


	def create_x_test_blending(self, X_test):
		#print(X_test)
		x_pred_test = self.transform_base_models(X_test)
		X_test_blending = np.hstack((X_test, x_pred_test))
		#print(X_test_blending)
		return X_test_blending

	def transform_meta_classifier_probabilities(self, X_blend):	
		model_probabilities = get_probabilities(self.copy_meta_model, X_blend)
		return model_probabilities

	def transform_meta_classifier_predictions(self, X_blend):
		model_predictions = get_predictions(self.copy_meta_model, X_blend)
		return model_predictions

	def predict_proba(self, X_test):
		X_blend = self.create_x_test_blending(X_test)
		probabilities = self.transform_meta_classifier_probabilities(X_blend)
		return probabilities

	def predict(self, X_test):
		X_blend = self.create_x_test_blending(X_test)
		predictions = self.transform_meta_classifier_predictions(X_blend)
		return predictions
	


