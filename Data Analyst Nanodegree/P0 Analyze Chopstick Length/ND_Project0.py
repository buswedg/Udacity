
# coding: utf-8

# In[2]:

from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')


# #Data Analyst Nanodegree
# ##Project 0: Analyze Chopstick Length

# A few researchers set out to determine the optimal length of chopsticks for children and adults. They came up with a measure of how effective a pair of chopsticks performed, called the "Food Pinching Performance." The "Food Pinching Performance" was determined by counting the number of peanuts picked and placed in a cup (PPPC).
# 
# ####An investigation for determining the optimum length of chopsticks.
# [Link to Abstract and Paper](http://www.ncbi.nlm.nih.gov/pubmed/15676839)  
# *the abstract below was adapted from the link*
# 
# Chopsticks are one of the most simple and popular hand tools ever invented by humans, but have not previously been investigated by [ergonomists](https://www.google.com/search?q=ergonomists). Two laboratory studies were conducted in this research, using a [randomised complete block design](http://dawg.utk.edu/glossary/whatis_rcbd.htm), to evaluate the effects of the length of the chopsticks on the food-serving performance of adults and children. Thirty-one male junior college students and 21 primary school pupils served as subjects for the experiment to test chopsticks lengths of 180, 210, 240, 270, 300, and 330 mm. The results showed that the food-pinching performance was significantly affected by the length of the chopsticks, and that chopsticks of about 240 and 180 mm long were optimal for adults and pupils, respectively. Based on these findings, the researchers suggested that families with children should provide both 240 and 180 mm long chopsticks. In addition, restaurants could provide 210 mm long chopsticks, considering the trade-offs between ergonomics and cost.
# 
# ####For the rest of this project, answer all questions based only on the part of the experiment analyzing the thirty-one adult male college students.
# Download the [data set for the adults](https://www.udacity.com/api/nodes/4576183932/supplemental_media/chopstick-effectivenesscsv/download), then answer the following questions based on the abstract and the data set.
# 
# **If you double click on this cell**, you will see the text change so that all of the formatting is removed. This allows you to edit this block of text. This block of text is written using [Markdown](http://daringfireball.net/projects/markdown/syntax), which is a way to format text using headers, links, italics, and many other options. You will learn more about Markdown later in the Nanodegree Program. Hit shift + enter or shift + return to show the formatted text.

# ####1. What is the independent variable in the experiment?
# Chopstick.Length

# ####2. What is the dependent variable in the experiment?
# Food.Pinching.Efficiency

# ####3. How is the dependent variable operationally defined?
# Mean efficiency for each chopstick length; determined by the number of peanuts picked and placed in a cup.

# ####4. Based on the description of the experiment and the data set, list at least two variables that you know were controlled.
# Age group
# Sex (participants were male)

# One great advantage of ipython notebooks is that you can document your data analysis using code, add comments to the code, or even add blocks of text using Markdown. These notebooks allow you to collaborate with others and share your work. For now, let's see some code for doing statistics.

# In[4]:

import pandas as pd


# In[6]:

path = r'data\chopstick-effectiveness.csv'
dataFrame = pd.read_csv(path)
dataFrame


# Let's do a basic statistical calculation on the data using code! Run the block of code below to calculate the average "Food Pinching Efficiency" for all 31 participants and all chopstick lengths.

# In[7]:

print "Food Pinching Mean:"
dataFrame['Food.Pinching.Efficiency'].mean()


# This number is helpful, but the number doesn't let us know which of the chopstick lengths performed best for the thirty-one male junior college students. Let's break down the data by chopstick length. The next block of code will generate the average "Food Pinching Effeciency" for each chopstick length. Run the block of code below.

# In[8]:

meansByChopstickLength = dataFrame.groupby('Chopstick.Length')['Food.Pinching.Efficiency'].mean().reset_index()

print "Mean by Chopstick Length:"
meansByChopstickLength

# reset_index() changes Chopstick.Length from an index to column. Instead of the index being the length of the chopsticks, the index is the row numbers 0, 1, 2, 3, 4, 5.


# ####5. Which chopstick length performed the best for the group of thirty-one male junior college students?
# 240mm

# In[9]:

# Causes plots to display within the notebook rather than in a new window
get_ipython().magic(u'pylab inline')

import matplotlib.pyplot as plt

plt.scatter(x=meansByChopstickLength['Chopstick.Length'], y=meansByChopstickLength['Food.Pinching.Efficiency'])
            # title="")
plt.xlabel("Length in mm")
plt.ylabel("Efficiency in PPPC")
plt.title("Average Food Pinching Efficiency by Chopstick Length")
plt.show()


# ####6. Based on the scatterplot created from the code above, interpret the relationship you see. What do you notice?
# Average efficiency increased on average as chopstick length grew from 160mm to 240mm, and decreased on average as chopstick length fell from 240mm to 340mm.

# ####In the abstract the researchers stated that their results showed food-pinching performance was significantly affected by the length of the chopsticks, and that chopsticks of about 240 mm long were optimal for adults.
# 
# ####7a. Based on the data you have analyzed, do you agree with the claim?
# No
# 
# ####7b. Why?
# Although the results of the research support this claim, I do not a) agree with the researchers definition/method of ranking chopstick efficiency, b) believe the sample size was large enough, and c) believe there were enough controlled variables i.e. past experience with using chopsticks?

# In[ ]:



