# Instead of geom_line(), use geom_smooth() to add a smoother to the plot.
# You can use the defaults for geom_smooth() but do color the line
# by year_joined.bucket

# ALTER THE CODE BELOW THIS LINE
# ==============================================================================

library("ggplot2")

pf <- read.delim('data/pseudo_facebook.tsv')

pf$year_joined <- floor(2014 - pf$tenure / 365)
pf$year_joined.bucket <- cut(pf$year_joined, breaks = c(2004, 2009, 2011, 2012, 2014))

data = subset(pf, tenure >= 1)

plot <- ggplot(data = data, aes(y = friendships_initiated/tenure, x = tenure)) + 
  geom_smooth(aes(color = year_joined.bucket))

print(plot)