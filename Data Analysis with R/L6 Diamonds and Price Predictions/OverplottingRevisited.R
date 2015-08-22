# Add a layer to adjust the features of the
# scatterplot. Set the transparency to one half,
# the size to three-fourths, and jitter the points.

# If you need hints, see the Instructor Notes.
# There are three hints so scroll down slowly if
# you don't want all the hints at once.

# ALTER THE CODE BELOW THIS LINE
# =======================================================================

library("scales")
library("ggplot2")

data(diamonds)

cuberoot_trans = function() trans_new('cuberoot', 
  transform = function(x) x^(1/3),
  inverse = function(x) x^3)

plot <- ggplot(data = diamonds, aes(y = price, x = carat)) + 
  geom_point(position = 'jitter', size = 0.75, alpha = 1/2) + 
  scale_x_continuous(trans = cuberoot_trans(), limits = c(0.2, 3),
    breaks = c(0.2, 0.5, 1, 2, 3)) + 
  scale_y_continuous(trans = log10_trans(), limits = c(350, 15000),
    breaks = c(350, 1000, 5000, 10000, 15000)) +
  ggtitle('Price (log10) by Cube-Root of Carat')

print(plot)