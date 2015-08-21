# Create a histogram of price per carat
# and facet it by cut. You can make adjustments
# to the code from the previous exercise to get
# started.

# Adjust the bin width and transform the scale
# of the x-axis using log10.

# Submit your final code when you are ready.

# ENTER YOUR CODE BELOW THIS LINE.
# ===========================================================================

library("ggplot2")
data("diamonds")

plot <- ggplot(diamonds, aes(x = price/carat)) + 
  geom_histogram(color = "Black", fill = "Blue") + 
  facet_grid(cut~., scale = "free") +
  ylab("Count") +
  xlab("Price per Carat")

print(plot)