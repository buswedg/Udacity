# This programming assignment
# will not be graded, but when you
# submit your code, the assignment
# will be marked as correct. By submitting
# your code, we can add to the feedback
# messages and address common mistakes
# in the Instructor Notes.

# You can assess your work by watching
# the solution video.


# Create a scatterplot of likes_received (y)
# vs. www_likes_received (x). Use any of the
# techniques that you've learned so far to
# modify the plot.

# ENTER ALL OF YOUR CODE TO CREATE THE PLOT BELOW THIS LINE.
# ===========================================================

library("ggplot2")

pf <- read.table("data/pseudo_facebook.tsv", header = TRUE)

plot <- ggplot(data = pf, aes(y = likes_received, x = www_likes_received)) +
  geom_point()

print(plot)