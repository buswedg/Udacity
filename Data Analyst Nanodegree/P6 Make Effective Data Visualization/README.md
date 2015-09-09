
#Make Effective Data Visualization
###Project: ND_Project6


###Introduction
This repository holds results for the Udacity Nanodegree Project: Make Effective Data Visualizations. For this project, I selected the 'flights' dataset and exercised d3.js in order to make an interactive map of the USA which allows visualization of flight delay statistics for various airports.


###Data
Flight delay statistics for this project were originally sourced from the Bureau of Transportation Statistics. The dataset contains 15 statistics on airports located within the USA, arranged by time and airport. This formed the primary dataset for this project, however additional data was also obtained from Openflights (airport latitude and longitude data) which was used to plot the location of each airport on the USA map. More information on each dataset and their source can be found in the data.Rmd file within this repo.


###Summary
The purpose of this visualization is to provide the ability to easily access and interpret timeseries flight delay statistics for various airports spread across the USA. The hope is that a potential user of this visualization can get a sense of 1) the likelihood a flight will be delayed (by airport), 2) the likelihood of reason a flight will be delayed (by airport), and 3) the relative and trending performance of flight an airport in terms to its delays to flights.


###Design
For this project, I sketched out two potential visualization designs. The first had a single plot element located to the right of the browser window with some dynamic data elements within a table on the left of the browser window. I imagined this design working similarly to a Excel PivotChart whereby the user could make cuts of the data as they pleased with the plot element updated in real-time.

After some research, I discovered a d3.js map which displays airport routes upon initiating a mouseover event for each airport located on a map of the USA. The map is part of the d3.js example library and can be found here [d3.js Symbol Map](http://mbostock.github.io/d3/talk/20111116/airports.html). From this, I sketched a second design which had a similar map on the left of the browser window and a plot element on the right. The intent was to allow the user to select an airport of interest located on the USA map and to have the plot element update to reflect the selected airport.

The second design was achieved through employing a combination of html, css, d3.js, dimple.js and R for back-end data wrangling.


###Feedback
Feedback was collected from three users throughout development of the visualization. This feedback was collected face-to-face while the user accessed a version of the visualization through Git Pages. For each user, I asked them: "if could make only one change to the visualization, what change would it be?". The feedback from these users and the changes made to the visualization are noted below:

User: Sarah
Feedback: "Improve descriptions of 'reasons for delays'." 
Update: The first version of the visualization had on a few words explaining each reason for delay category. Upon receiving this feedback, I spent some time searching the original data source and expanded each description.

User: Ben
Feedback: "Have the airport name popup when hovering over the location on the USA map."
Update: For the visualization version which Ben reviewed, the airport name would show for the airport above the USA map only after it had been selected. Upon receiving this feedback, I added a feature which would show the airport name when hovering over its location.

User: Allex
Feedback: "Include a link to the original data source."
Update: Originally, no link was provided to the original data source. Upon receiving this feedback, I added a link below the visualization title.
