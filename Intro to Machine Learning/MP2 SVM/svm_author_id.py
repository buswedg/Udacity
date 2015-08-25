# %load svm_author_id.py
#!/usr/bin/python

""" 
   this is the code to accompany the Lesson 2 (SVM) mini-project

   use an SVM to identify emails from the Enron corpus by their authors
   
   Sara has label 0
   Chris has label 1

"""
   
import sys
from time import time
from email_preprocess import preprocess
from sklearn.svm import SVC


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

#features_train = features_train[:len(features_train)/100]
#labels_train = labels_train[:len(labels_train)/100]

#clf = SVC(kernel='linear')
clf = SVC(kernel='rbf',C=10000)
clf.fit(features_train,labels_train)

predict = clf.predict(features_test)

print "What is the accuracy of your author identification SVM?"
score = clf.score(features_test,labels_test)
print score

print "How do the training and prediction times compare to Naive Bayes?"
t0 = time()
clf.fit(features_train,labels_train)
print 'train time', round(time()-t0,3)

t0 = time()
clf.score(features_test,labels_test)
print 'predict time', round(time()-t0,3)

print "What class does your SVM (0 or 1, corresponding to Sara and Chris respectively) predict for element 10 of the test set? The 26th? The 50th?"
print predict[10]
print predict[26]
print predict[50]

print "There are over 1700 test events--how many are predicted to be in the “Chris” (1) class?"
n = []
[n.append(i) for i in pred if i == 1]
len(n)

#########################################################