# Create a scatter plot of the price/carat ratio
# of diamonds. The variable x should be
# assigned to cut. The points should be colored
# by diamond color, and the plot should be
# faceted by clarity.

# The plot should look something like this.
# http://i.imgur.com/YzbWkHT.jpg.

# Note: In the link, a color palette of type
# 'div' was used to color the histogram using
# scale_color_brewer(type = 'div')

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================

library("ggplot2")

data(diamonds)

plot <- ggplot(data = diamonds, aes(x = cut, y = price/carat)) +
  geom_point(aes(color = diamonds$color), alpha = (1/2), position = position_jitter(width = 0.3)) +
  facet_wrap( ~ clarity)

print(plot)