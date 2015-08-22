# Create a new variable in the data frame
# called year_joined.bucket by using
# the cut function on the variable year_joined.

# You need to create the following buckets for the
# new variable, year_joined.bucket

#        (2004, 2009]
#        (2009, 2011]
#        (2011, 2012]
#        (2012, 2014]

# Note that a parenthesis means exclude the year and a
# bracket means include the year.

# Look up the documentation for cut or try the link
# in the Instructor Notes to accomplish this task.

# DO NOT DELETE THE TWO LINES OF CODE BELOW THIS LINE
# ========================================================================
pf <- read.delim('data/pseudo_facebook.tsv')
pf$year_joined <- floor(2014 - pf$tenure / 365)

# ENTER YOUR CODE BELOW THIS LINE
# ========================================================================

pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))