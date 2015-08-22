# Let's start by examining two variables in the data set.
# The scatterplot is a powerful tool to help you understand
# the relationship between two continuous variables.

# We can quickly see if the relationship is linear or not.
# In this case, we can use a variety of diamond
# characteristics to help us figure out whether
# the price advertised for any given diamond is 
# reasonable or a rip-off.

# Let's consider the price of a diamond and it's carat weight.
# Create a scatterplot of price (y) vs carat weight (x).

# Limit the x-axis and y-axis to omit the top 1% of values.

# ENTER YOUR CODE BELOW THIS LINE
# ================================================================

library("ggplot2")

data(diamonds)

plot <- ggplot(data = diamonds, aes(y = price, x = carat)) +
  geom_point() +
  coord_cartesian(xlim = c(0, quantile(diamonds$carat, 0.99)),
    ylim = c(0, quantile(diamonds$price, 0.99))) +
  stat_smooth(method = "lm")

print(plot)