# Your task is to build five linear models like Solomon
# did for the diamonds data set only this
# time you'll use a sample of diamonds from the
# diamondsbig data set.

# Be sure to make use of the same variables
# (logprice, carat, etc.) and model
# names (m1, m2, m3, m4, m5).

# To get the diamondsbig data into RStudio
# on your machine, copy, paste, and run the
# code in the Instructor Notes. There's
# 598,024 diamonds in this data set!

# Since the data set is so large,
# you are going to use a sample of the
# data set to compute the models. You can use
# the entire data set on your machine which
# will produce slightly different coefficients
# and statistics for the models.

# This exercise WILL BE automatically graded.

# You can leave off the code to load in the data.
# We've sampled the data for you.
# You also don't need code to create the table output of the models.
# We'll do that for you and check your model summaries (R^2 values, AIC, etc.)

# Your task is to write the code to create the models.

# DO NOT ALTER THE CODE BELOW THIS LINE (Reads in a sample of the diamondsbig data set)
#===========================================================================================
load("data/BigDiamonds.Rda")


# ENTER YOUR CODE BELOW THIS LINE. (Create the five models)
#===========================================================================================
m1 <- lm( I(log(price)) ~ I(carat^(1/3)), 
  data = subset(diamondsbig, price < 10000 & cert == 'GIA' ))
m2 <- update(m1, ~  . + carat)
m3 <- update(m2, ~ . + cut)
m4 <- update(m3, ~ . + color)
m5 <- update(m4, ~ . + clarity)


# DO NOT ALTER THE CODE BELOW THIS LINE (Tables your models and pulls out the statistics)
#===========================================================================================
suppressMessages(library(lattice))
suppressMessages(library(MASS))
suppressMessages(library(memisc))
models <- mtable(m1, m2, m3, m4, m5)