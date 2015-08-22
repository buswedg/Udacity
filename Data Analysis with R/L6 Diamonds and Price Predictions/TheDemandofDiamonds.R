# Create two histograms of the price variable
# and place them side by side on one output image.

# We've put some code below to get you started.

# The first plot should be a histogram of price
# and the second plot should transform
# the price variable using log10.

# Set appropriate bin widths for each plot.
# ggtitle() will add a title to each histogram.

# You can self-assess your work with the plots
# in the solution video.

# ALTER THE CODE BELOW THIS LINE
# ==============================================

library("gridExtra")
library("ggplot2")

data(diamonds)

plot1 <- ggplot(data = diamonds, aes(x = price)) +
  geom_histogram() +
  ggtitle('Price')

plot2 <- ggplot(data = diamonds, aes(x = price)) +
  geom_histogram() +
  scale_x_log10() +
  ggtitle('Price(log10)')

grid.arrange(plot1, plot2)