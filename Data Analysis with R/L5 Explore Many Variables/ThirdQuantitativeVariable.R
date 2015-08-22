# Create a variable called year_joined
# in the pf data frame using the variable
# tenure and 2014 as the reference year.

# The variable year joined should contain the year
# that a user joined facebook.

# See the Instructor Notes for three hints if you get
# stuck. Scroll down slowly to see one hint at a time
# if you would like some guidance.

# This programming exercise WILL BE automatically graded.

# DO NOT ALTER THE CODE BELOW THIS LINE
# ========================================================
pf <- read.delim('data/pseudo_facebook.tsv')

# ENTER YOUR CODE BELOW THIS LINE.
# ========================================================

pf$year_joined <- floor(2014 - pf$tenure/365)