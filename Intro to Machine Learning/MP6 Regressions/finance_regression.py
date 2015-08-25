#%load finance_regression.py
#!/usr/bin/python

"""
   starter code for the regression mini-project
   
   loads up/formats a modified version of the dataset
   (why modified?  we've removed some trouble points
   that you'll find yourself in the outliers mini-project)

   draws a little scatterplot of the training/testing data

   you fill in the regression code where indicated

"""    


import sys
import pickle
from feature_format import featureFormat, targetFeatureSplit
dictionary = pickle.load( open("data/final_project_dataset_modified.pkl", "r") )
%matplotlib inline

### list the features you want to look at--first item in the 
### list will be the "target" feature
features_list = ["bonus", "salary"]
#features_list = ["bonus", "long_term_incentive"]
data = featureFormat( dictionary, features_list, remove_any_zeroes=True )
target, features = targetFeatureSplit( data )

### training-testing split needed in regression, just like classification
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
feature_train, feature_test, target_train, target_test = train_test_split(features, target, test_size=0.5, random_state=42)
train_color = "b"
test_color = "b"



### Your regression goes here!
### Please name it reg, so that the plotting code below picks it up and 
### plots it correctly. Don't forget to change the test_color from "b" to "r"
### to differentiate training points from test points.

reg = linear_model.LinearRegression()
reg.fit(feature_train,target_train)

predict = reg.predict(feature_test)

print "What are the slope and intercept?"
slope = reg.coef_
print slope

intercept = reg.intercept_
print intercept

print "What is the score of the regression on the training data?"
score = reg.score(feature_train,target_train)
print score

print "What is the score of the regression on the testing data?"
score = reg.score(feature_test,target_test)
print score

print "Now we’ll be drawing two regression lines, one fit on the test data (with outlier) and one fit on the training data (no outlier). What’s the slope of the new regression line?"
### draw the scatterplot, with color-coded training and testing points
import matplotlib.pyplot as plt
for feature, target in zip(feature_test, target_test):
   plt.scatter( feature, target, color=test_color ) 
for feature, target in zip(feature_train, target_train):
   plt.scatter( feature, target, color=train_color ) 

### labels for the legend
plt.scatter(feature_test[0], target_test[0], color=test_color, label="test")
plt.scatter(feature_test[0], target_test[0], color=train_color, label="train")


### draw the regression line, once it's coded
try:
   plt.plot( feature_test, reg.predict(feature_test) )
except NameError:
   pass
reg.fit(feature_test, target_test)
plt.plot(feature_train, reg.predict(feature_train), color="r")

slope = reg.coef_
print slope

plt.xlabel(features_list[1])
plt.ylabel(features_list[0])
plt.legend()
plt.show()