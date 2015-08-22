# Create a new variable called all.purchases,
# which gives the total counts of yogurt for
# each observation or household.

# One way to do this is using the transform
# function. You can look up the function transform
# and run the examples of code at the bottom of the
# documentation to figure out what it does.

# The transform function produces a data frame
# so if you use it then save the result to 'yo'!

# OR you can figure out another way to create the
# variable.

# DO NOT ALTER THE CODE BELOW THIS LINE
# ========================================================
yo <- read.csv('data/yogurt.csv')

# ENTER YOUR CODE BELOW THIS LINE
# ========================================================

yo <- transform(yo, all.purchases = strawberry + blueberry + pina.colada + plain + mixed.berry)