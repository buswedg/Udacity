# Create a new variable, 'age_with_months', in the 'pf' data frame.
# Be sure to save the variable in the data frame rather than creating
# a separate, stand-alone variable. You will need to use the variables
# 'age' and 'dob_month' to create the variable 'age_with_months'.

# Assume the reference date for calculating age is December 31, 2013.

# This programming assignment WILL BE automatically graded. For
# this exercise, you need only create the 'age_with_months' variable;
# no further processing of the data frame is necessary.

# DO NOT DELETE THIS NEXT LINE OF CODE
# ========================================================================
pf <- read.delim('data/pseudo_facebook.tsv')


# ENTER YOUR CODE BELOW THIS LINE
# ========================================================================
pf$age_with_months <- pf$age + (1.0 - pf$dob_month / 12)