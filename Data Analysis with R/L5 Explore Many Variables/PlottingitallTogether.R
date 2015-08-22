# Create a line graph of friend_count vs. age
# so that each year_joined.bucket is a line
# tracking the median user friend_count across
# age. This means you should have four different
# lines on your plot.

# You should subset the data to exclude the users
# whose year_joined.bucket is NA.

# If you need a hint, see the Instructor Notes.

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===================================================

library("ggplot2")

pf <- read.delim('data/pseudo_facebook.tsv')

pf$year_joined <- floor(2014 - pf$tenure / 365)
pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))

plot <- ggplot(data = subset(pf, !is.na(year_joined.bucket)), aes(x = age, y = friend_count)) +
  geom_line(aes(color = year_joined.bucket), stat = 'summary', fun.y = median)

print(plot)