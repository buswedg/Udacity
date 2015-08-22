# Change the code to make the transparency of the
# points to be 1/100 of what they are now and mark
# the x-axis every 2 units. See the instructor notes
# for two hints.

# This assignment is not graded and
# will be marked as correct when you submit.

# ALTER THE CODE BELOW THIS LINE
#============================================

library("ggplot2")
data("diamonds")

plot <- ggplot(data = diamonds, aes(y = price, x = depth)) +
  geom_point() +
  scale_x_continuous(breaks = seq(0, 80, 2))

print(plot)