# Smooth the last plot you created of
# of prop_initiated vs tenure colored by
# year_joined.bucket. You can use larger
# bins for tenure or add a smoother to the plot.

# There won't be a solution image for this exercise.
# You will answer some questions about your plot in
# the next two exercises.

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ====================================================

library("ggplot2")

pf <- read.delim('data/pseudo_facebook.tsv')

pf$prop_initiated = pf$friendships_initiated / pf$friend_count
pf$year_joined <- floor(2014 - pf$tenure/365)
pf$year_joined.bucket <- cut(pf$year_joined, c(2004, 2009, 2011, 2012, 2014))

pf = subset(pf, !is.na(year_joined.bucket))

ggplot(data = pf, aes(y = prop_initiated, x = tenure, color = year_joined.bucket)) +
  geom_line(stat = 'summary', fun.y = mean) +
  geom_smooth()