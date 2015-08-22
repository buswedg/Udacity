# Create a line graph showing the
# median friend count over the ages
# for each gender. Be sure to use
# the data frame you just created,
# pf.fc_by_age_gender.

# See the Instructor Notes for a hint.

# This assignment is not graded and
# will be marked as correct when you submit.

# ENTER YOUR CODE BELOW THIS LINE
# =================================================

library("dplyr")
library("ggplot2")

pf <- read.delim('data/pseudo_facebook.tsv')

pf.fc_by_age_gender <- pf %>%
  filter(!is.na(gender)) %>%
  group_by(age, gender) %>%
  summarize(mean_friend_count = mean(friend_count),
  median_friend_count = median(as.numeric(friend_count)), 
  n = n())

plot <- ggplot(data = pf.fc_by_age_gender, aes(y = median_friend_count, x = age)) +
  geom_line(aes(color = gender))

print(plot)