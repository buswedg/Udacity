
# coding: utf-8

# In[3]:

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
# ##Project 2: Analyzing the NYC Subway Dataset

# ###Section 1. Statistical Test

# ####1.1 Which statistical test did you use to analyze the NYC subway data? Did you use a one-tail or a two-tail P value? What is the null hypothesis? What is your p-critical value?
# 
# ####1.2 Why is this statistical test applicable to the dataset? In particular, consider the assumptions that the test is making about the distribution of ridership in the two samples. 
# 
# The Mann-Whitney U-test was used to compare the mean ridership of rainy days vs non-rainy days. This test is suitable as the underlying distributions are not normally distributed (non-parametric test).
# 
# A two-tail test and hence a two-tail P value was used. The two-tail test is suitable as the test is to establish whether there is any significant difference in means of the two datasets (positive or negative).
# 
# Null Hypothesis: There 'is no significant difference' in population average ridership on rainy days compared to the average ridership on non-rainy days.
# 
# Alternative Hypothesis: There 'is a significant difference' in population average ridership on rainy days compared to the average ridership on non-rainy days.

# In[4]:

import pandas as pd
import numpy as np
import scipy.stats


# In[5]:

path = r'data\turnstile_weather_v2.csv'
dataFrame = pd.read_csv(path)
dataFrame


# In[6]:

df_rain = dataFrame[dataFrame.rain != 0]
df_norain = dataFrame[dataFrame.rain == 0]

df_rainent = df_rain['ENTRIESn_hourly']
df_norainent = df_norain['ENTRIESn_hourly']


# ###1.3 What results did you get from this statistical test? These should include the following numerical values: p-values, as well as the means for each of the two samples under test. 
# 
# ###1.4 What is the significance and interpretation of these results?

# In[7]:

print "Mean ridership for rain group:"
df_rainent.mean()


# In[8]:

print "Standard deviation of ridership for rain group:"
df_rainent.std()


# In[9]:

print "Mean ridership for non-rain group:"
df_norainent.mean()


# In[10]:

print "Standard deviation of ridership for non-rain group:"
df_norainent.std()


# The mean ridership for the rain group is higher than the non-rain group, however ridership datapoints for the rain group also have greater standard deviation than the non-rain group. Below forms the test for statistically significant difference between mean ridership of the two groups.

# In[11]:

n = len(df_rain)

print "Number of observations with rain:"
n


# In[12]:

n = len(df_norain)

print "Number of observations without rain:"
n


# In[11]:

# Note: Followed 'Method Two' (see: https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test) to find the critical 
# value, as the sample size is > ~20 and therefore U is assumed to be approximately normally distributed.


# In[13]:

U,p = scipy.stats.mannwhitneyu(df_rainent, df_norainent)
m_u = (len(df_rainent) * len(df_norainent)) / 2
sigma_u = np.sqrt(len(df_rainent) * len(df_norainent) * (len(df_rainent) + len(df_norainent) + 1) / 12)
z = (U - m_u) / sigma_u
p = 2 * scipy.stats.norm.cdf(z)

print "Mann-Whitney U-test statistic:"
p


# We reject the Null Hypothesis that there 'is no significant difference' in population average ridership on rainy days compared to the average ridership on non-rainy days at the 5% significance level. (5.48e-06 < 0.05)

# ###Section 2. Linear Regression

# ####2.1 What approach did you use to compute the coefficients theta and produce prediction for ENTRIESn_hourly in your regression model: OLS using Statsmodels or Scikit Learn, Gradient descent using Scikit Learn, Or something different?
# 
# ####2.2 What features (input variables) did you use in your model? Did you use any dummy variables as part of your features?
# 
# ####2.3 Why did you select these features in your model? We are looking for specific reasons that lead you to believe that the selected features will contribute to the predictive power of your model. 

# OLS (using statsmodels) was used to compute the coefficients theta and produce prediction for ENTRIESn_hourly (hourly number of entries).
# 
# Features considered in the model include:
# 1) 'hour': Expectation that ridership varies based on the time of day (peak vs. non-peak transit hours).
# 2) 'weekday': Expectation that ridership varies based on weekdays vs. weekends (business vs. leisure transit).
# 3) 'UNIT': A transformed dummy variable to account for higher/lower trafficked units. This is to account for disparity between stations average ridership due to (for example) whether the station is located in a heavy/less populated area.
# 
# Note that 'rain', 'fog' and 'tempi' were also considered, however they were not found to significantly increase the predictive power (R2) of the model.

# In[14]:

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[15]:

path = r'data\turnstile_weather_v2.csv'
dataFrame = pd.read_csv(path)
#dataFrame


# In[16]:

y = dataFrame['ENTRIESn_hourly']

x = dataFrame[['hour', 'weekday']]
#x = dataFrame[['hour', 'weekday', 'rain', 'fog', 'tempi']]

unit_dum = pd.get_dummies(dataFrame['UNIT'], prefix = 'unit')
x = x.join(unit_dum)


# In[17]:

result = sm.OLS(y, x).fit()


# ###2.4 What are the parameters (also known as "coefficients" or "weights") of the non-dummy features in your linear regression model?
# 
# ###2.5 What is your model’s R2 (coefficients of determination) value?

# In[18]:

result.rsquared
result.summary()


# In[19]:

pred = result.predict(x)
(y - pred).mean()


# The final R2 (coefficient of determination) value for the fitted model was 0.481. That is, just over 48% of the variation of number of ENTRIESn_hourly (hourly number of entries) can be explained by the included features: 'hour' (time of day), 'weekday' (day of week), and 'UNIT' (accounting for the disparity in average ridership between stations).
# 
# The low R2 value suggests that caution should be exercised when using this model in order to generate a prediction of future ridership.

# ###Section 3. Visualization

# ####Please include two visualizations that show the relationships between two or more variables in the NYC subway data. Remember to add appropriate titles and axes labels to your plots. Also, please add a short description below each figure commenting on the key insights depicted in the figure. 

# In[20]:

import pandas as pd
import numpy as np
import itertools as itr
import matplotlib.pyplot as plt
from ggplot import * ## requires ggplot: $ pip install ggplot, also note: https://github.com/yhat/ggplot/issues/417
get_ipython().magic(u'matplotlib inline')


# In[21]:

path = r'data\turnstile_weather_v2.csv'
df_raw = pd.read_csv(path)
#df_raw


# In[22]:

#df_rain = df_raw[df_raw.rain != 0]
#df_rain = df_raw.reset_index(drop = True)


# In[23]:

#plot_rainent = ggplot(df_rain, aes(x = 'ENTRIESn_hourly')) +\
#    geom_histogram() +\
#    ggtitle('Total Hourly Entries (Obs with Rain)') +\
#    xlab('Entries Range') +\
#    ylab('Density')
#
#plot_rainent


# In[24]:

#df_norain = df_raw[df_raw.rain == 0]
#df_norain = df_raw.reset_index(drop = True)


# In[25]:

#plot_norainent = ggplot(df_norain, aes(x = 'ENTRIESn_hourly')) +\
#    geom_histogram() +\
#    ggtitle('Total Hourly Entries (Obs without Rain)') +\
#    xlab('Entries Range') +\
#    ylab('Density')
#
#plot_norainent


# In[26]:

plot_entbyrain = ggplot(df_raw, aes('ENTRIESn_hourly', fill = 'rain')) +    geom_histogram(position = 'dodge') +    facet_wrap('rain') +    ggtitle("Total Hourly Entries (Obs with(top)/without(bottom) Rain)") +    xlab('Entries Range') +    ylab('Density')
    
plot_entbyrain


# Data suggests a similar distribution for entry data on days where it rained vs. days where it did not rain. Note the greater amount of entry observations (distribution height) were recorded on days where it did not rain.

# In[27]:

df_raw.station.unique()
df_sumbystat = df_raw.groupby('station', as_index = False).sum()
df_sumbystat = df_sumbystat.sort('ENTRIESn_hourly')


# In[28]:

df_sumbytopstat = df_sumbystat[-10:]
df_sumbytopstat


# In[29]:

#plot_sumentbydow = ggplot(df_sumbytopstat, aes(x = 'station', y = 'ENTRIESn')) \
#    + geom_bar(stat = 'identity') \
#    + ggtitle('Total Entries by Station') \
#    + xlab('Station') \
#    + ylab('Total Entries')
#plot_sumentbydow


# In[30]:

# The number of entries varies greatly depending on the station. Ridership is greatest for '34 ST-HERALD SQ' and
# '34 ST-PENN STA'.


# In[31]:

df_sumbybotstat = df_sumbystat[:10]
df_sumbybotstat


# In[32]:

#plot_sumentbydow = ggplot(df_sumbybotstat, aes(x = 'station', y = 'ENTRIESn')) \
#    + geom_bar(stat = 'identity') \
#    + ggtitle('Total Entries by Station') \
#    + xlab('Station') \
#    + ylab('Total Entries')
#plot_sumentbydow


# In[33]:

# Ridership is lowest for 'OXFORD-104 ST' and '215 ST'.


# In[34]:

df_sumentbydow = df_raw.groupby('day_week', as_index = False).sum()
df_meanentbydow = df_raw.groupby('day_week', as_index = False).mean()


# In[35]:

plot_sumentbydow = ggplot(df_sumentbydow, aes(x = 'day_week', y = 'ENTRIESn_hourly'))     + geom_bar(stat = 'identity')     + ggtitle('Total Entries by Day of Week')     + xlab('Day of Week (0 = Monday)')     + ylab('Total Entries')
plot_sumentbydow


# In[36]:

plot_meanentbydow = ggplot(df_meanentbydow, aes(x = 'day_week', y = 'ENTRIESn_hourly'))     + geom_bar(stat = 'identity')     + ggtitle('Average Entries by Day of Week')     + xlab('Day of Week (0 = Monday)')     + ylab('Average Entries')
plot_meanentbydow


# Total/average entry data over a single week shows that weekdays have greater ridership than weekends.

# In[37]:

df_sumentbyhr = df_raw.groupby('hour', as_index = False).sum()
df_meanentbyhr = df_raw.groupby('hour', as_index = False).mean()


# In[38]:

plot_sumentbyhr = ggplot(df_sumentbyhr, aes(x = 'hour', y = 'ENTRIESn_hourly'))     + geom_bar(stat = 'identity')     + ggtitle('Total Entries by Hour of Day')     + xlab('Hour of Day (0 = 12:00am)')     + ylab('Total Entries')
plot_sumentbyhr


# In[39]:

plot_meanentbyhr = ggplot(df_meanentbyhr, aes(x = 'hour', y = 'ENTRIESn_hourly'))     + geom_bar(stat = 'identity')     + ggtitle('Average Entries by Hour of Day')     + xlab('Hour of Day (0 = 12:00am)')     + ylab('Total Entries')
plot_meanentbyhr


# Average entry data over a single day shows a greater ridership from midday onwards.

# ###Section 4. Conclusion

# ####4.1 From your analysis and interpretation of the data, do more people ride the NYC subway when it is raining or when it is not raining?  
# ####4.2 What analyses lead you to this conclusion? You should use results from both your statistical tests and your linear regression to support your analysis.

# From the analysis and interpretation of data, I have concluded that (for the provided dataset) people did tend to ride the subway in New York more often on days which had rain compared to days which did not have rain. This is supported by the conducted Mann-Whitney U Test outlined above. 
# 
# However, when estimating an OLS relationship for ridership, I found that rain did not provide any significant benefit to the models predictive power. Instead, the day of week provided much greater predictive power. Suitability of an OLS model for this dataset may be a concern, however this result suggests to me that more observations of days with/without rain over each day of the week would be beneficial in determining whether rain is able to effect the level of ridership.

# ###Section 5. Reflection

# ####5.1 Please discuss potential shortcomings of the methods of your analysis, including: Dataset, Analysis, such as the linear regression model or statistical test.
# ####5.2 (Optional) Do you have any other insight about the dataset that you would like to share with us?

# The dataset is one of the major shortcomings of this analysis. Although there is a fair amount of scope to the data in terms of number of features, it contains observations for only a single month (May 2011). This can lead to inconsistencies in recognizing relationships between data variables but also has the potential to hide longer-term relationships such as seasonality factors. The decision to opt for only a single type of linear model and to make no mathematical transformations to the modelled variables may also prove as shortcomings of this analysis.
