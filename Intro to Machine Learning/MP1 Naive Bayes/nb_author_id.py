# %load nb_author_id.py
#!/usr/bin/python

""" 
   this is the code to accompany the Lesson 1 (Naive Bayes) mini-project 

   use a Naive Bayes Classifier to identify emails by their authors
   
   authors and labels:
   Sara has label 0
   Chris has label 1

"""
   
import sys
from time import time
from email_preprocess import preprocess
from sklearn.naive_bayes import GaussianNB


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

clf = GaussianNB()
clf.fit(features_train,labels_train)



print "What is the accuracy of your Naive Bayes author identifier?"
score = clf.score(features_test,labels_test)
print score

print "What is faster, training or prediction?"
t0 = time()
clf.fit(features_train,labels_train)
print 'train time', round(time()-t0,3)

t0 = time()
clf.score(features_test,labels_test)
print 'predict time', round(time()-t0,3)

#########################################################