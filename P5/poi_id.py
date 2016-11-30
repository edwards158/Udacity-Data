#!/usr/bin/python

#%matplotlib inline
import sys
import pickle
sys.path.append("../tools/")
import pylab
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
from json import dumps
from time import time
import math
import sklearn
import json
from sklearn.metrics import accuracy_score
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, f_classif,SelectPercentile

import pprint

### The first feature must be "poi".
poi = ['poi']

features_financial = [
            #    "bonus",
                "deferral_payments",
                "deferred_income",
            #    "director_fees",
            #    "exercised_stock_options",
            #    "expenses",
            #   "loan_advances",
            #    "long_term_incentive",
            #    "other",
            #    "restricted_stock",
             #   "restricted_stock_deferred",
            #    "salary",
            #    "total_payments",
            #    "total_stock_value"
                ]
features_email = [
                "from_messages",
                "from_poi_to_this_person",
                "from_this_person_to_poi",
                "shared_receipt_with_poi",
                "to_messages",
                #"email_address"
                ]

features_list_new = [ 
    #    "ratio_poi_messages",
    #    "salary_log",
    #    "bonus_log",
    #    "total_payments_log",
    #    "deferral_payments_log",  
    #    "deferred_income_log", 
    #    "director_fees_log",  
    #    "exercised_stock_options_log",  
    #    "expenses_log", 
    #    "loan_advances_log",  
    #    "long_term_incentive_log",
    #    "other_log", 
    #    "restricted_stock_deferred_log", 
    #    "restricted_stock_log", 
    #    "total_stock_value_log",
    #    "ratio_bonus_total_payments",
    #    "ratio_salary_total_payments"
]

features_list = poi + features_financial + features_email

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

my_dataset = data_dict
### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)    

labels, features = targetFeatureSplit(data)

#remove the outliers
outliers = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK']
for outlier in outliers:
    data_dict.pop(outlier, 0)


#make new variables based on emails
for name in data_dict:
    try:
        total_messages = data_dict[name]['from_messages'] + data_dict[name]['to_messages']
        poi_related_messages = data_dict[name]["from_poi_to_this_person"] +\
                                    data_dict[name]["from_this_person_to_poi"] +\
                                    data_dict[name]["shared_receipt_with_poi"]
        data_dict[name]['ratio_poi_messages'] = (1.0 * poi_related_messages / total_messages)
    except:
        data_dict[name]['ratio_poi_messages'] = 'NaN'

#take log of monetary based features
for name in data_dict:
    for feature in features_financial:
        try:
            data_dict[name][feature + '_log'] = math.log(data_dict[name][feature]+1)      
        except:
            data_dict[name][feature + '_log'] = 'NaN'

#make ratio of salary to total payments
for name in data_dict:
    try:
        data_dict[name]['ratio_salary_total_payments'] = 1.0 *data_dict[name]['salary']\
        / data_dict[name]['total_payments']
    except:
        data_dict[name]['ratio_salary_total_payments'] = 'NaN'
#make ratio of bonus to total payments
for name in data_dict:
    try:
        data_dict[name]['ratio_bonus_total_payments'] = 1.0 *data_dict[name]['bonus']\
        / data_dict[name]['total_payments']
    except:
        data_dict[name]['ratio_bonus_total_payments'] = 'NaN'

features_list = poi  + features_financial+ features_list_new + features_email
print features_list

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

#apply min max scaling
scaler = preprocessing.MinMaxScaler()
features = scaler.fit_transform(features)

#function is not called as not used in final test
k = 15
def generate_k_best(data_dict, features_list, k):
    #Run SelectKbest - returns a dictionary of best features
    select_k_best = SelectKBest(k=k)
    select_k_best.fit(features, labels)
    scores = select_k_best.scores_
    unsorted_pairs = zip(features_list[1:], scores)
    sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
    k_best_features = dict(sorted_pairs[:k])
    return k_best_features

#k_best = generate_k_best(data_dict, features_list, 15)
#print "{0} best features are: {1}\n".format(k, k_best.keys())
#features_list = poi + k_best.keys()
print features_list


t0 = time()
ab_clf = AdaBoostClassifier()
scores = sklearn.cross_validation.cross_val_score(ab_clf, features, labels,cv =3)
print "Ada Boost scores: " ;print scores
print "Ada Boost Time:", round(time()-t0, 3), "s\n"

t0 = time()
gnb_clf = GaussianNB()
scores = sklearn.cross_validation.cross_val_score(gnb_clf, features, labels, cv=3)
print "Naive Bayes scores: " ;print scores
print "Naive Bayes Time:", round(time()-t0, 3), "s\n"

t0 = time()
lsvc_clf = LinearSVC()
scores = sklearn.cross_validation.cross_val_score(lsvc_clf, features, labels, cv = 3)
print "Linear SVC  scores: " ;print scores
print "Linear SVC Time:", round(time()-t0, 3), "s\n"

t0 = time()
lr_clf = LogisticRegression()
scores = sklearn.cross_validation.cross_val_score(lr_clf, features, labels, cv = 3)
print "Logistic regression  scores: " ;print scores
print "Logistic regression Time:", round(time()-t0, 3), "s\n"

## Create Cross Validation object for use in GridSearchCV
cv = sklearn.cross_validation.StratifiedShuffleSplit(labels, 1000, random_state = 42)

#clf = LogisticRegression(C=1.0, class_weight='balanced', dual=False,
#          fit_intercept=True, intercept_scaling=1, max_iter=100,
#          multi_class='ovr', n_jobs=1, penalty='l1', random_state=None,
#          solver='liblinear', tol=0.0001, verbose=0, warm_start=False)


clf = LogisticRegression(C=100, class_weight='balanced', dual=False,
      fit_intercept=True, intercept_scaling=1, max_iter=100,
      multi_class='ovr', n_jobs=1, penalty='l1', random_state=None,
      solver='liblinear', tol=0.0001, verbose=0, warm_start=False)

#Linear SVC
#clf = LinearSVC()
#params_lsvc = {"C": [0.5, 1.0, 10, 100, 1000],"class_weight":['balanced'],"penalty":['l1','l2'],
#                        "dual":[False]
#                        }

#Logistic Regression
#clf = LogisticRegression()
#params_lrg = {"C": [0.5, 1.0, 10,100,1000],"class_weight":['balanced'],"penalty":['l1','l2'],
#                        "dual":[False]
#                        }
#Naive Gaussian Bayes
#clf = GaussianNB()

#AdaBoost
#params_ada = {"n_estimators" : [10,50,100,200]}
#clf = AdaBoostClassifier()

#Decision Tree
#clf = DecisionTreeClassifier()
#params_dtc = {"min_samples_split": [5,10,20,50]}

## Apply GridSearchCV to the dataset
#clf = GridSearchCV(clf, params_lrg, scoring = 'f1', cv=cv)
clf.fit(features, labels)

## Set the best performing combination of parameters as the new classifier
#clf = clf.best_estimator_

## Use included tester function to assess performance using cross validation
test_classifier(clf, my_dataset, features_list)

dump_classifier_and_data(clf, my_dataset, features_list)
