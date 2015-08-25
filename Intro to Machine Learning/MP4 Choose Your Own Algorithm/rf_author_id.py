#!/usr/bin/python

""" 
   this is the code to accompany the Lesson 3 (decision tree) mini-project

   use an DT to identify emails from the Enron corpus by their authors
   
   Sara has label 0
   Chris has label 1

"""
   
import sys
from time import time
from email_preprocess import preprocess
from sklearn.ensemble import RandomForestClassifier


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

#features_train = features_train[:len(features_train)/100]
#labels_train = labels_train[:len(labels_train)/100]

clf = RandomForestClassifier()
clf.fit(features_train,labels_train)

predict = clf.predict(features_test)

print "What is the accuracy of your decision tree?"
score = clf.score(features_test,labels_test)
print score

print "What's the number of features in your data?"
feat = len(features_train[0])
print feat

#########################################################