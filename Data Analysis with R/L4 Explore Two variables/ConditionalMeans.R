# This programming assignment
# will not be graded, but when you
# submit your code, the assignment
# will be marked as correct. By submitting
# your code, we can add to the feedback
# messages and address common mistakes
# in the Instructor Notes.

# You can assess your work by watching
# the solution video.


# Plot mean friend count vs. age using a line graph.
# Be sure you use the correct variable names
# and the correct data frame. You should be working
# with the new data frame created from the dplyr
# functions. The data frame is called 'pf.fc_by_age'.

# Use geom_line() rather than geom_point to create
# the plot. You can look up the documentation for
# geom_line() to see what it does.

# ENTER ALL OF YOUR CODE TO CREATE THE PLOT BELOW THIS LINE.
# ===========================================================

library("dplyr")
library("ggplot2")

pf <- read.table("data/pseudo_facebook.tsv", header = TRUE)

age_groups <- group_by(pf, age)

pf.fc_by_age <- summarise(age_groups,
  friend_count_mean = mean(friend_count),
  friend_count_median = median(friend_count),
  n = n())

pf.fc_by_age <- arrange(pf.fc_by_age, age)

plot <- ggplot(data = pf.fc_by_age, aes(y = friend_count_mean, x = age)) + 
  geom_line()

print(plot)