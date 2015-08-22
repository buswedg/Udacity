# Create a simple scatter plot of price vs depth.

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
#==================================================

library("ggplot2")
data("diamonds")

plot <- ggplot(data = diamonds, aes(y = price, x = depth)) +
  geom_point()

print(plot)