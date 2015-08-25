# %load vectorize_text.py

#!/usr/bin/python

import os
import pickle
import re
import sys
import nltk
#nltk.download()
from parse_out_email_text import parseOutText
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer

"""
    starter code to process the emails from Sara and Chris to extract
    the features and get the documents ready for classification

    the list of all the emails from Sara are in the from_sara list
    likewise for emails from Chris (from_chris)

    the actual documents are in the Enron email dataset, which
    you downloaded/unpacked in Part 0 of the first mini-project

    the data is stored in lists and packed away in pickle files at the end

"""


from_sara  = open("data/from_sara.txt", "r")
from_chris = open("data/from_chris.txt", "r")

from_data = []
word_data = []

### temp_counter is a way to speed up the development--there are
### thousands of emails from Sara and Chris, so running over all of them
### can take a long time
### temp_counter helps you only look at the first 200 emails in the list
#temp_counter = 0


for name, from_person in [("sara", from_sara), ("chris", from_chris)]:
    for path in from_person:
        ### only look at first 200 emails when developing
        ### once everything is working, remove this line to run over full dataset
        #temp_counter += 1
        #if temp_counter < 200:
            #Point to maildir path of Udacity Intro to ML repo
            path = "" + path[:-1]
            #print path
            email = open(path, "r")

            ### use parseOutText to extract the text from the opened email
            words = parseOutText(email)

            ### use str.replace() to remove any instances of the words
            ### ["sara", "shackleton", "chris", "germani"]
            #replace_words  = ["sara", "shackleton", "chris", "germani"]
            replace_words  = ["sara", "shackleton", "chris", "germani", "sshacklensf", "cgermannsf"]
            for i in replace_words:
                words = words.replace(i,"")
            
            ### append the text to word_data
            word_data.append(words)
            
            ### append a 0 to from_data if email is from Sara, and 1 if email is from Chris
            from_data.append(0 if name == "sara" else 1)

            email.close()

            
print "emails processed"
from_sara.close()
from_chris.close()

pickle.dump( word_data, open("data/your_word_data.pkl", "w") )
pickle.dump( from_data, open("data/your_email_authors.pkl", "w") )

print "What is the string for word_data[152]?"
print word_data[152]
#print len(word_data)

### in Part 4, do TfIdf vectorization here
print "How many stopwords are there?"
sw = stopwords.words("english")
print len(sw)

vectorizer = TfidfVectorizer(stop_words="english")
vec = vectorizer.fit_transform(word_data)

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(vec)

print "How many unique words are in your Tfldf?"
#bw = vectorizer.transform(word_data)
print len(vectorizer.get_feature_names())

print "What is word number 34597 in your TfIdf?"
vectorizer.get_feature_names()[34597]

#print "What is word number 33614 in your TfIdf?"
#vectorizer.get_feature_names()[33614]

#print "What is word number 33614 in your TfIdf?"
#vectorizer.get_feature_names()[14343]