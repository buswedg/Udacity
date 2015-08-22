# This programming assignment
# will not be graded, but when you
# submit your code, the assignment
# will be marked as correct. By submitting
# your code, we can add to the feedback
# messages and address common mistakes
# in the Instructor Notes.

# You can assess your work by watching
# the solution video.


# Examine the relationship between
# friendships_initiated (y) and age (x)
# using the ggplot syntax.

# We recommend creating a basic scatter
# plot first to see what the distribution looks like.
# and then adjusting it by adding one layer at a time.

# What are your observations about your final plot?

# Remember to make adjustments to the breaks
# of the x-axis and to use apply alpha and jitter.

# ENTER ALL OF YOUR CODE FOR YOUR PLOT BELOW THIS LINE.
# =======================================================

library("ggplot2")

pf <- read.table("data/pseudo_facebook.tsv", header = TRUE)

plot <- ggplot(data = pf, aes(y = friendships_initiated, x = age, color = gender)) +
  geom_point()

print(plot)