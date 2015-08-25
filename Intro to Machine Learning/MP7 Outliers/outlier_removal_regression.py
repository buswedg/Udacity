# %load outlier_removal_regression.py
#!/usr/bin/python

import random
import numpy
import matplotlib.pyplot as plt
import pickle
from sklearn import linear_model
%matplotlib inline


#from outlier_cleaner import outlierCleaner
def outlierCleaner(predictions, ages, net_worths):
   """
       clean away the 10% of points that have the largest
       residual errors (different between the prediction
       and the actual net worth)

       return a list of tuples named cleaned_data where 
       each tuple is of the form (age, net_worth, error)
   """
   
   cleaned_data = []
   
   ### your code goes here
  
   netwerr = (net_worths-predictions)**2
   databyerr = zip(ages,net_worths,netwerr)
   databyerr = sorted(databyerr,key=lambda x:x[2][0],reverse=True)
   sortlimit = int(len(databyerr)*0.1)
   
   cleaned_data = databyerr[sortlimit:]
   
   return cleaned_data



### load up some practice data with outliers in it
ages = pickle.load( open("data/practice_outliers_ages.pkl", "r") )
net_worths = pickle.load( open("data/practice_outliers_net_worths.pkl", "r") )


### ages and net_worths need to be reshaped into 2D numpy arrays
### second argument of reshape command is a tuple of integers: (n_rows, n_columns)
### by convention, n_rows is the number of data points
### and n_columns is the number of features
ages       = numpy.reshape( numpy.array(ages), (len(ages), 1))
net_worths = numpy.reshape( numpy.array(net_worths), (len(net_worths), 1))
from sklearn.cross_validation import train_test_split
ages_train, ages_test, net_worths_train, net_worths_test = train_test_split(ages, net_worths, test_size=0.1, random_state=42)

### fill in a regression here!  Name the regression object reg so that
### the plotting code below works, and you can see what your regression looks like

reg = linear_model.LinearRegression()

reg.fit(ages_train,net_worths_train)

cleaned_data = outlierCleaner(reg.predict(ages_train),ages_train,net_worths_train)
cleaned_age = numpy.array([i[0] for i in cleaned_data])
cleaned_netw = numpy.array([i[1] for i in cleaned_data])

#reg.fit(cleaned_age,cleaned_netw)
reg.fit(ages_train,net_worths_train)

predict = reg.predict(net_worths_test)

print "What's the slope of your regression?"
slope = reg.coef_
print slope

intercept = reg.intercept_
print intercept

print "What's the score when using your regression to make predictions with the test data?"
score = reg.score(ages_test,net_worths_test)
print score


try:
   plt.plot(ages, reg.predict(ages), color="blue")
except NameError:
   pass
plt.scatter(ages, net_worths)
plt.show()



### identify and remove the most outlier-y points
cleaned_data = []
try:
   predictions = reg.predict(ages_train)
   cleaned_data = outlierCleaner( predictions, ages_train, net_worths_train )
except NameError:
   print "your regression object doesn't exist, or isn't name reg"
   print "can't make predictions to use in identifying outliers"



### only run this code if cleaned_data is returning data
if len(cleaned_data) > 0:
   ages, net_worths, errors = zip(*cleaned_data)
   ages       = numpy.reshape( numpy.array(ages), (len(ages), 1))
   net_worths = numpy.reshape( numpy.array(net_worths), (len(net_worths), 1))

   ### refit your cleaned data!
   try:
       reg.fit(ages, net_worths)
       plt.plot(ages, reg.predict(ages), color="blue")
   except NameError:
       print "you don't seem to have regression imported/created,"
       print "   or else your regression object isn't named reg"
       print "   either way, only draw the scatter plot of the cleaned data"
   plt.scatter(ages, net_worths)
   plt.xlabel("ages")
   plt.ylabel("net worths")
   plt.show()


else:
   print "outlierCleaner() is returning an empty list, no refitting to be done"