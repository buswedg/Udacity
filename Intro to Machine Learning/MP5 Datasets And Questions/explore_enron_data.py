# %load explore_enron_data.py

#!/usr/bin/python

""" 
   starter code for exploring the Enron dataset (emails + finances) 
   loads up the dataset (pickled dict of dicts)

   the dataset has the form
   enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

   {features_dict} is a dictionary of features associated with that person
   you should explore features_dict as part of the mini-project,
   but here's an example to get you started:

   enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
   
"""

import pickle

enron_data = pickle.load(open("data/final_project_dataset.pkl", "r"))

print "How many data points (people) are in the dataset?"
points = len(enron_data.keys())
print points

print "For each person, how many features are available?",
perfeat = len(enron_data[enron_data.keys()[0]].keys())
print perfeat

print "How many POIs are there in the E+F dataset?"
poi_count = 0
for k in enron_data:
   if enron_data[k]["poi"] == 1:
       poi_count += 1

print poi_count

print "What is the total value of the stock belonging to James Prentice?"
jpstock = enron_data['PRENTICE JAMES']['total_stock_value']
print jpstock

print "How many email messages do we have from Wesley Colwell to persons of interest?"
wcemail = enron_data['COLWELL WESLEY']['from_this_person_to_poi']
print wcemail 

print "What’s the value of stock options exercised by Jeffrey Skilling?"
jsstock = enron_data['SKILLING JEFFREY K']['exercised_stock_options']
print jsstock

print "How many folks in this dataset have a quantified salary?"
quantified_salary_count = 0
for k in enron_data:
   if enron_data[k]['salary'] != 'NaN':
       quantified_salary_count += 1

print quantified_salary_count

print "What about a known email address?"
email_address_count = 0
for k in enron_data:
   if enron_data[k]['salary'] != 'NaN':
       email_address_count += 1

print email_address_count