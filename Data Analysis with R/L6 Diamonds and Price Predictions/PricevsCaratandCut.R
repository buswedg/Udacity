# Let's look at cut and see if we find a similar result.

# Adjust the code below to color the points by cut.
# Change any other parts of the code as needed.

# ALTER THE CODE BELOW THIS LINE
# =========================================================================================

library("scales")
library("ggplot2")

data(diamonds)

cuberoot_trans = function() trans_new('cuberoot', 
  transform = function(x) x^(1/3),
  inverse = function(x) x^3)

plot <- ggplot(data = diamonds, aes(y = price, x = carat, color = cut)) + 
  geom_point(alpha = 0.5, size = 1, position = 'jitter') +
  scale_x_continuous(trans = cuberoot_trans(), limits = c(0.2, 3),
    breaks = c(0.2, 0.5, 1, 2, 3)) + 
  scale_y_continuous(trans = log10_trans(), limits = c(350, 15000),
    breaks = c(350, 1000, 5000, 10000, 15000)) +
  ggtitle('Price (log10) by Cube-Root of Carat and Cut')

print(plot)