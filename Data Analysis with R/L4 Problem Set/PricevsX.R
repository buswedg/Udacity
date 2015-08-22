# In this problem set, you'll continue
# to explore the diamonds data set.

# Your first task is to create a
# scatterplot of price vs x.
# using the ggplot syntax.

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================

library("ggplot2")
data("diamonds")

plot <- ggplot(data = diamonds, aes(y = x, x = price)) +
  geom_point()

print(plot)