# Create a histogram of the price of
# all the diamonds in the diamond data set.

# TYPE YOUR CODE BELOW THE LINE
# =======================================

library("ggplot2")
data("diamonds")

plot <- ggplot(diamonds, aes(x = price)) + 
  geom_histogram(color = "Black", fill = "Blue", binwidth = 500) + 
  scale_x_continuous(breaks = seq(0, 20000, 1000)) + 
  ylab("Count") +
  xlab("Price")

print(plot)