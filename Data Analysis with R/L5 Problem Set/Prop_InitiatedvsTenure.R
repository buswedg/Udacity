# Create a line graph of the median proportion of
# friendships initiated ('prop_initiated') vs.
# tenure and color the line segment by
# year_joined.bucket.

# Recall, we created year_joined.bucket in Lesson 5
# by first creating year_joined from the variable tenure.
# Then, we used the cut function on year_joined to create
# four bins or cohorts of users.

# (2004, 2009]
# (2009, 2011]
# (2011, 2012]
# (2012, 2014]

# The plot should look something like this.
# http://i.imgur.com/vNjPtDh.jpg
# OR this
# http://i.imgur.com/IBN1ufQ.jpg

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================================

library("ggplot2")

pf <- read.delim('data/pseudo_facebook.tsv')

pf$prop_initiated = pf$friendships_initiated / pf$friend_count
pf$year_joined <- floor(2014 - pf$tenure/365)
pf$year_joined.bucket <- cut(pf$year_joined, c(2004, 2009, 2011, 2012, 2014))

pf = subset(pf, !is.na(year_joined.bucket))

plot <- ggplot(data = pf, aes(y = prop_initiated, x = tenure, color = year_joined.bucket)) +
  geom_line(stat = 'summary', fun.y = mean)

print(plot)