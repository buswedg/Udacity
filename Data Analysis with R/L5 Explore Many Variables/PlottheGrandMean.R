# Write code to do the following:

# (1) Add another geom_line to code below
# to plot the grand mean of the friend count vs age.

# (2) Exclude any users whose year_joined.bucket is NA.

# (3) Use a different line type for the grand mean.

# As a reminder, the parameter linetype can take the values 0-6:

# 0 = blank, 1 = solid, 2 = dashed
# 3 = dotted, 4 = dotdash, 5 = longdash
# 6 = twodash

# This assignment is not graded and
# will be marked as correct when you submit.

# The code from the last programming exercise should
# be your starter code!

# ENTER YOUR CODE BELOW THIS LINE
# ==================================================================

library("ggplot2")

pf <- read.delim('data/pseudo_facebook.tsv')

pf$year_joined <- floor(2014 - pf$tenure / 365)
pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))

pf = subset(pf, !is.na(year_joined.bucket))

plot <- ggplot(data = pf, aes(y = friend_count, x = age)) +
  geom_line(aes(color = year_joined.bucket), stat = 'summary', fun.y = mean) +
  geom_line(stat = 'summary', fun.y = mean, linetype = 2)

print(plot)