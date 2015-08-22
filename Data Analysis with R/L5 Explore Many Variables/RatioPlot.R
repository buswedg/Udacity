# Plot the ratio of the female to male median
# friend counts using the data frame
# pf.fc_by_age_gender.wide.

# Think about what geom you should use.
# Add a horizontal line to the plot with
# a y intercept of 1, which will be the
# base line. Look up the documentation
# for geom_hline to do that. Use the parameter
# linetype in geom_hline to make the
# line dashed.

# The linetype parameter can take the values 0-6:
# 0 = blank, 1 = solid, 2 = dashed
# 3 = dotted, 4 = dotdash, 5 = longdash
# 6 = twodash

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# =================================================

library("dplyr")
library("reshape2")
library("ggplot2")

pf <- read.delim('data/pseudo_facebook.tsv')

pf.fc_by_age_gender <- pf %>%
  filter(!is.na(gender)) %>%
  group_by(age, gender) %>%
  summarize(mean_friend_count = mean(friend_count),
  median_friend_count = median(as.numeric(friend_count)), 
  n = n())

pf.fc_by_age_gender.wide <- dcast(pf.fc_by_age_gender, age ~ gender, value.var = 'median_friend_count')

plot <- ggplot(data = pf.fc_by_age_gender.wide, aes(y = female / male, x = age)) +
  geom_line()

print(plot)