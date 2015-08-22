# This programming assignment
# will not be graded, but when you
# submit your code, the assignment
# will be marked as correct. By submitting
# your code, we can add to the feedback
# messages and address common mistakes
# in the Instructor Notes.

# You can assess your work by watching
# the solution video.


# Create a new scatterplot showing friend_count_mean
# versus the new variable, age_with_months. Be sure to use
# the correct data frame (the one you create in the last
# exercise) AND subset the data to investigate
# users with ages less than 71.

# ENTER YOUR CODE BELOW THIS LINE.
# ===============================================================

library("dplyr")

pf <- read.delim('data/pseudo_facebook.tsv')
pf$age_with_months <-pf$age + (1 - pf$dob_month / 12)

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

pf = filter(pf.fc_by_age_months, age_with_months <= 71)

ggplot(data = pf, aes(y = friend_count_mean, x = age_with_months)) +
  geom_line()