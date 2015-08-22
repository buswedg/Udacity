# Create a new data frame called
# pf.fc_by_age_months that contains
# the mean friend count, the median friend
# count, and the number of users in each
# group of age_with_months. The rows of the
# data framed should be arranged in increasing
# order by the age_with_months variable.

# For example, the first two rows of the resulting
# data frame would look something like...

# age_with_months  friend_count_mean	friend_count_median	n
#              13            275.0000                   275 2
#        13.25000            133.2000                   101 11


# See the Instructor Notes for two hints if you get stuck.
# This programming assignment will automatically be graded.

# DO NOT DELETE THESE NEXT THREE LINES OF CODE
# ========================================================================
pf <- read.delim('data/pseudo_facebook.tsv')
pf$age_with_months <-pf$age + (1 - pf$dob_month / 12)

# ENTER YOUR CODE BELOW THIS LINE
# ========================================================================
library("dplyr")

age_months_groups <- group_by(pf, age_with_months)

pf.fc_by_age_months <- summarise(age_months_groups,
  friend_count_mean = mean(friend_count),
  friend_count_median = median(friend_count),
  n = n())

pf.fc_by_age_months <- arrange(pf.fc_by_age_months, age_with_months)

pf.fc_by_age_monthsc <- pf%>%
  group_by(age_with_months)%>%
  summarise(friend_count_mean = mean(friend_count),
    friend_count_median = median(friend_count),
    n = n())%>%
  arrange(age_with_months)