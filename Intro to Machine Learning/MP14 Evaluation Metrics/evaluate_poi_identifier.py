# %load evaluate_poi_identifier.py
#!/usr/bin/python


"""
    starter code for the validation mini-project
    the first step toward building your POI identifier!

    start by loading/formatting the data

    after that, it's not our code anymore--it's yours!
"""

import pickle
import sys
import numpy
from feature_format import featureFormat, targetFeatureSplit
from sklearn import cross_validation
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from collections import Counter

data_dict = pickle.load(open("data/final_project_dataset.pkl", "r") )

### first element is our labels, any added elements are predictor
### features. Keep this the same for the mini-project, but you'll
### have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

features_train,features_test,labels_train,labels_test = cross_validation.train_test_split(features,labels,test_size=0.3, random_state=42)

clf = DecisionTreeClassifier()

fit = clf.fit(features_train,labels_train)
predict = clf.predict(features_test)
score1 = clf.score(features_test,labels_test)

print "Accuracy:"
print score1

print "How many POIs are in the test set for your POI identifier?"
numpy.array(labels_test)
POI = len([i for i in labels_test if i == 1.0])
print POI

print "How many people total are in your test set?"
people = len(labels_test)
print people

print "If your identifier predicted 0. (not POI) for everyone in the test set, what would its accuracy be?"
score2 = 1.0-(float(POI) / float(people))
print score2

print "How mnay true positives are there?"
confusion_matrix = Counter()
binary_truth = [x in positives for x in labels_test]
binary_prediction = [x in positives for x in predict]
for t, p in zip(binary_truth, binary_prediction):
    confusion_matrix[t,p] += 1

print confusion_matrix

print "What's the precision of your POI identifier?"
precision = precision_score(predict, labels_test)
print precision

print "What's the recall of your POI identifier?"
recall = recall_score(predict, labels_test)
print recall

predict = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1]
truth = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]

print "How many true/false positives/negatives are there?"
confusion_matrix = Counter()
binary_truth = [x in positives for x in truth]
binary_prediction = [x in positives for x in predict]
for t, p in zip(binary_truth, binary_prediction):
    confusion_matrix[t,p] += 1

print confusion_matrix

print "What's the precision of your POI identifier?"
precision = precision_score(predict, truth)
print precision

print "What's the recall of your POI identifier?"
recall = recall_score(predict, truth)
print recall