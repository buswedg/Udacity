# Subset the data to exclude diamonds with a volume
# greater than or equal to 800. Also, exclude diamonds
# with a volume of 0. Adjust the transparency of the
# points and add a linear model to the plot. (See the
# Instructor Notes or look up the documentation of
# geom_smooth() for more details about smoothers.)

# We encourage you to think about this next question and
# to post your thoughts in the discussion section.

# Do you think this would be a useful model to estimate
# the price of diamonds? Why or why not?

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ========================================

library("ggplot2")
data("diamonds")

diamonds$volume <- diamonds$x * diamonds$y * diamonds$z

diamonds = subset(diamonds, (volume > 0) & (volume <= 800))

plot <- ggplot(data = diamonds, aes(x = volume, y = price)) +
  geom_point() +
  geom_smooth()

print(plot)