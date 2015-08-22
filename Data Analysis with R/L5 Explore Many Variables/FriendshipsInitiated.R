# Create a line graph of mean of friendships_initiated per day (of tenure)
# vs. tenure colored by year_joined.bucket.

# You need to make use of the variables tenure,
# friendships_initiated, and year_joined.bucket.

# You also need to subset the data to only consider user with at least
# one day of tenure.

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ========================================================================

library("ggplot2")

pf <- read.delim('data/pseudo_facebook.tsv')

pf$year_joined <- floor(2014 - pf$tenure / 365)
pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))

pf = subset(pf, tenure >= 1)

plot <- ggplot(data = pf, aes(y = friendships_initiated/tenure, x = tenure)) + 
  geom_line(aes(color = year_joined.bucket), stat = 'summary', fun.y = mean)

print(plot)