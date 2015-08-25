# %load validate_poi.py
#!/usr/bin/python

"""
    starter code for the validation mini-project
    the first step toward building your POI identifier!

    start by loading/formatting the data

    after that, it's not our code anymore--it's yours!
"""

import pickle
import sys
from feature_format import featureFormat, targetFeatureSplit
from sklearn import cross_validation
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

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

print "What's the accuracy/accuracy with a testing regime properly deployed?"
score = clf.score(features_test,labels_test)
print score

### it's all yours from here forward!  