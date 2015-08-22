# Order the factor levels in the age.range variable in order to create
# a graph with a natural order. Look up the documentation for
# the factor function or read through the example in the Instructor Notes.

# Once you're ready, try to write the code to order the levels of
# the age.range variable.

# Be sure you modify the variable in the data frame. That is modify reddit$age.range.
# Don't create a new variable.

# The levels of age.range should take on these values...

#    "Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 or Above"

# This exercise is ungraded. You can check your own work by using the Test Run
# button. Your plot will appear there.

# ENTER YOUR CODE BELOW THE LINE.
# ================================================================================

library("ggplot2")

reddit <- read.csv("data/reddit.csv")

reddit$age.range <- ordered(reddit$age.range, levels = c("Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65, Above"))

qplot(data = reddit, x = age.range)