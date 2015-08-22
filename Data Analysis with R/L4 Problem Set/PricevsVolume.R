# Create a scatterplot of price vs. volume (x * y * z).
# This is a very rough approximation for a diamond's volume.

# Create a new variable for volume in the diamonds data frame.
# This will be useful in a later exercise.

# Don't make any adjustments to the plot just yet.

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# =================================================================

library("ggplot2")
data("diamonds")

diamonds$volume <- diamonds$x * diamonds$y * diamonds$z

plot <- ggplot(data = diamonds, aes(y = price, x = volume)) +
  geom_point()

print(plot)