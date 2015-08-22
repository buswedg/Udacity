# Create a scatterplot of price vs time.

# This will be an example of a time series plot.

# Resolve overplotting issues by using
# techniques you learned in Lesson 4.

# What are some things that you notice?

# ENTER YOUR CODE BELOW THIS LINE
# ================================================

yo <- read.csv('data/yogurt.csv')

yo <- transform(yo, all.purchases = strawberry + blueberry + pina.colada + plain + mixed.berry)

plot <- ggplot(data = yo, aes(y = price, x = time)) +
  geom_point(alpha = .05)

print(plot)