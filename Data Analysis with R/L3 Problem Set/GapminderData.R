# The Gapminder website contains over 500 data sets with information about
# the world's population. Your task is to download a data set of your choice
# and create 2-5 plots that make use of the techniques from Lesson 3.

# You might use a simple histogram, a boxplot split over a categorical variable,
# or a frequency polygon. The choice is yours!

# You can find a link to the Gapminder website in the Instructor Notes.

# Once you've completed your investigation, create a post in the discussions that includes:
#       1. any questions you answered, your observations, and summary statistics
#       2. snippets of code that created the plots
#       3. links to the images of your plots

# You can save images by using the ggsave() command.
# ggsave() will save the last plot created.
# For example...
#                  qplot(x = price, data = diamonds)
#                  ggsave('priceHistogram.png')

# ggsave currently recognises the extensions eps/ps, tex (pictex),
# pdf, jpeg, tiff, png, bmp, svg and wmf (windows only).

# Copy and paste all of the code that you used for
# your investigation, and submit it when you are ready.
# ====================================================================================

library("xlsx")
library("reshape2")
library("dplyr")
library("ggplot2")

hours <- tbl_df(read.xlsx("data/indicator_hours per week.xlsx", sheetName = "Data", header = TRUE))

hours <- hours %>%
  select(-NA.) %>%
  rename(Country = Working.hours.per.week) %>%
  filter(Country != "<NA>")

hours.long <- melt(hours, id = c("Country"), value.name = "Hours", variable.name = "Year")
hours.long <- tbl_df(hours.long)

hours.long <- hours.long %>%
  mutate(Year = as.character(Year),
         Year = substr(Year, 2, 5),
         Year = as.numeric(Year))

yearStats <- hours.long %>%
  group_by(Year) %>%
  summarise(median = median(Hours, na.rm = TRUE),
            mean = mean(Hours, na.rm = TRUE),
            lower = min(Hours, na.rm = TRUE),
            upper = max(Hours, na.rm = TRUE),
            se = sd(Hours, na.rm = TRUE)/sqrt(length(Hours)),
            avg_upper = mean + (2.101 * se),
            avg_lower = mean - (2.101 * se),
            quant.25 = quantile(Hours, na.rm = TRUE, 0.25),
            quant.75 = quantile(Hours, na.rm = TRUE, 0.75))

yearStats <- round(yearStats, 2)

plot <- ggplot(yearStats, aes(y = median, x = Year)) +
  geom_line()

print(plot)