# %load enron_outliers.py
#!/usr/bin/python

import pickle
import sys
import matplotlib.pyplot
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit


### read in data dictionary, convert to numpy array
data_dict = pickle.load( open("data/final_project_dataset.pkl", "r") )
features = ["salary", "bonus"]
data = featureFormat(data_dict, features)


### your code below
print "Show the outliers on a scatter plot"
print data.max()

for point in data:
   salary = point[0]
   bonus = point[1]
   plt.scatter( salary, bonus )

plt.xlabel("salary")
plt.ylabel("bonus")


print "What is the source of the most extreme outlier?"
data_dict.pop('TOTAL',0)


print "What are the names associated with the current Enron outliers?"
outliers = []
for key in data_dict:
   val = data_dict[key]['salary']
   if val == 'NaN':
       continue
   outliers.append((key,int(val)))

print sorted(outliers,key=lambda x:x[1],reverse=True)[:2]