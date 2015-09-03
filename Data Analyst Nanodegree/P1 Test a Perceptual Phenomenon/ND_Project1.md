

```python
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
```




<script>
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
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>



#Data Analyst Nanodegree
##Project 1: Test a Perceptual Phenomenon

###1. What is our independent variable? What is our dependent variable?

Independent variable: Word condition (i.e. Congruent or Incongruent), Dependent variable: Response time

###2. What is an appropriate set of hypotheses for this task? What kind of statistical test do you expect to perform? Justify your choices.

Null Hypothesis: There 'is no significant difference' in the population average response time viewing words which are congruent compared to average response time viewing words which are incongruent.

Alternative Hypothesis: There 'is a significant difference' in the population average response time viewing words which are congruent compared to average response time viewing words with are incongruent.

Expect to perform a paired-samples t-test as the same group of subjects have been assigned different word conditions from two different tests (matched pairs of similar units). Doing so would allow for increased statistical power compared to an ordinary unpaired test. (see: https://en.wikipedia.org/wiki/Paired_difference_test)

After taking the online test, I expect there will be statistically significant difference between average response times of the two conditions, as the second condition took noteably longer to complete.

###3. Report some descriptive statistics regarding this dataset. Include at least one measure of central tendency and at least one measure of variability.


```python
import pandas as pd
```


```python
path = r'data\stroopdata.csv'
dataFrame = pd.read_csv(path)
dataFrame
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Congruent</th>
      <th>Incongruent</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>12.079</td>
      <td>19.278</td>
    </tr>
    <tr>
      <th>1</th>
      <td>16.791</td>
      <td>18.741</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9.564</td>
      <td>21.214</td>
    </tr>
    <tr>
      <th>3</th>
      <td>8.630</td>
      <td>15.687</td>
    </tr>
    <tr>
      <th>4</th>
      <td>14.669</td>
      <td>22.803</td>
    </tr>
    <tr>
      <th>5</th>
      <td>12.238</td>
      <td>20.878</td>
    </tr>
    <tr>
      <th>6</th>
      <td>14.692</td>
      <td>24.572</td>
    </tr>
    <tr>
      <th>7</th>
      <td>8.987</td>
      <td>17.394</td>
    </tr>
    <tr>
      <th>8</th>
      <td>9.401</td>
      <td>20.762</td>
    </tr>
    <tr>
      <th>9</th>
      <td>14.480</td>
      <td>26.282</td>
    </tr>
    <tr>
      <th>10</th>
      <td>22.328</td>
      <td>24.524</td>
    </tr>
    <tr>
      <th>11</th>
      <td>15.298</td>
      <td>18.644</td>
    </tr>
    <tr>
      <th>12</th>
      <td>15.073</td>
      <td>17.510</td>
    </tr>
    <tr>
      <th>13</th>
      <td>16.929</td>
      <td>20.330</td>
    </tr>
    <tr>
      <th>14</th>
      <td>18.200</td>
      <td>35.255</td>
    </tr>
    <tr>
      <th>15</th>
      <td>12.130</td>
      <td>22.158</td>
    </tr>
    <tr>
      <th>16</th>
      <td>18.495</td>
      <td>25.139</td>
    </tr>
    <tr>
      <th>17</th>
      <td>10.639</td>
      <td>20.429</td>
    </tr>
    <tr>
      <th>18</th>
      <td>11.344</td>
      <td>17.425</td>
    </tr>
    <tr>
      <th>19</th>
      <td>12.369</td>
      <td>34.288</td>
    </tr>
    <tr>
      <th>20</th>
      <td>12.944</td>
      <td>23.894</td>
    </tr>
    <tr>
      <th>21</th>
      <td>14.233</td>
      <td>17.960</td>
    </tr>
    <tr>
      <th>22</th>
      <td>19.710</td>
      <td>22.058</td>
    </tr>
    <tr>
      <th>23</th>
      <td>16.004</td>
      <td>21.157</td>
    </tr>
  </tbody>
</table>
</div>




```python
print "Congruent mean:"
dataFrame['Congruent'].mean()
```

    Congruent mean:
    




    14.051125000000004




```python
print "Congruent standard deviation:"
dataFrame['Congruent'].std()
```

    Congruent standard deviation:
    




    3.559357957645195




```python
print "Incongruent mean:"
dataFrame['Incongruent'].mean()
```

    Incongruent mean:
    




    22.01591666666667




```python
print "Incongruent standard deviation:"
dataFrame['Incongruent'].std()
```

    Incongruent standard deviation:
    




    4.797057122469138



###4. Provide one or two visualizations that show the distribution of the sample data. Write one or two sentences noting what you observe about the plot or plots.


```python
dataFrame['Subject'] = dataFrame.index + 1
get_ipython().magic(u'pylab inline')

pylab.title('Congruent')
plt.ylabel('Completion time (seconds)')
plt.xlabel('Subject')
plt.scatter(x = dataFrame['Subject'], y = dataFrame['Congruent'])
            # title="")
```

    Populating the interactive namespace from numpy and matplotlib
    




    <matplotlib.collections.PathCollection at 0xe2fd278>




![png](output_12_2.png)



```python
pylab.title('Incongruent')
plt.ylabel('Completion time (seconds)')
plt.xlabel('Subject')
plt.scatter(x = dataFrame['Subject'], y = dataFrame['Incongruent'])
            # title="")
```




    <matplotlib.collections.PathCollection at 0xe44acc0>




![png](output_13_1.png)


The congruent words sample ranges between ~8 and ~22, while the incongruent words sample ranges between ~15 and ~35.

It is worth pointing out the two longest completion time samples (~34 & ~35) of the incongruent sample could be labeled as outliers from the wider sample set. These outliers will somewhat bias both the mean and standard deviation measures reported earlier, however the wider sample set confirms the greater reported mean.

###5. Now, perform the statistical test and report your results. What is your confidence level and your critical statistic value? Do you reject the null hypothesis or fail to reject it? Come to a conclusion in terms of the experiment task. Did the results match up with your expectations?


```python
n = len(dataFrame)

print "Number of observations:"
n
```

    Number of observations:
    




    24




```python
#### df = n - 1 = 23
#### t-critical values (two sided) for 90% confidence level:
#### 1.714 (see: https://en.wikipedia.org/wiki/Student's_t-distribution#Table_of_selected_values)
```


```python
#### Difference
dataFrame['Diff'] = dataFrame['Incongruent'] - dataFrame['Congruent']

#### Difference from mean
difffrommean = dataFrame['Diff'] - dataFrame['Diff'].mean()

#### Squared differences
dataFrame['SqDiff'] = difffrommean * difffrommean

#### Sum of squared differences
sumsquareddiff = dataFrame['SqDiff'].sum()

#### Sample statistic
v = sumsquareddiff / (n - 1)
s = sqrt(v)

print "Sample statistic:"
s
```

    Sample statistic:
    




    4.8648269103590556




```python
#### Point estimate
pointtest = dataFrame['Incongruent'].mean() - dataFrame['Congruent'].mean()

#### t-statistic
t = pointtest / (s / sqrt(n))

print "t-statistic:"
t
```

    t-statistic:
    




    8.0207069441099552



We reject the Null Hypothesis that there 'is no significant difference' in population average response time viewing words which  are congruent compared to average response time viewing words which are incongruent. (8.021 > 1.714)

This result is in-line with my expectations after taking the online test, which showed that the second condition took longer to complete.
