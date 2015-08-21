# Explore the largest peak in the
# price histogram you created earlier.

# Try limiting the x-axis, altering the bin width,
# and setting different breaks on the x-axis.

# There won't be a solution video for this
# question so go to the discussions to
# share your thoughts and discover
# what other people find.

# You can save images by using the ggsave() command.
# ggsave() will save the last plot created.
# For example...
#                  qplot(x = price, data = diamonds)
#                  ggsave('priceHistogram.png')

# ggsave currently recognises the extensions eps/ps, tex (pictex),
# pdf, jpeg, tiff, png, bmp, svg and wmf (windows only).

# Submit your final code when you are ready.

# TYPE YOUR CODE BELOW THE LINE
# ======================================================================

library("ggplot2")
data("diamonds")

plot <- ggplot(diamonds, aes(x = price)) + 
  geom_histogram(color = "Black", fill = "Blue", binwidth = 25) + 
  scale_x_continuous(limits = c(500, 1000)) + 
  ylab("Count") +
  xlab("Price")

print(plot)