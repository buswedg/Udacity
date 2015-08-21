# Create a histogram of the price of
# all the diamonds in the diamond data set.

# TYPE YOUR CODE BELOW THE LINE
# =======================================

library("ggplot2")
data("diamonds")

plot <- ggplot(diamonds, aes(x = price)) + 
  geom_histogram(color = "Black", fill = "Blue") + 
  facet_wrap(~cut, ncol = 2) + 
  ylab("Count") +
  xlab("Price")

print(plot)