# Create a scatterplot of diamond price vs.
# table and color the points by the cut of
# the diamond.

# The plot should look something like this.
# http://i.imgur.com/rQF9jQr.jpg

# Note: In the link, a color palette of type
# 'qual' was used to color the scatterplot using
# scale_color_brewer(type = 'qual')

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# ===========================================

library("ggplot2")

data(diamonds)

plot <- ggplot(data = diamonds, aes(y = price, x = table, color = cut)) +
  geom_point() +
  scale_x_continuous(breaks = seq(50, 80, 2), lim = c(50, 80)) 

print(plot)