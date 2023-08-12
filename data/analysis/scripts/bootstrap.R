##################
# Assessing Brazilian protected areas through social media: insights from 10 years of public interest and engagement
# Updated 11/08/2023
# R 4.1.1 
##################

library(readxl)
library(rcompanion)
library(tidyverse)
library(Hmisc)

#data
data <- readxl::read_xlsx("C:/Users/data_users.xlsx")
head(data)

#engagement
data$engage <- data$like_count + data$retweet_count

users <- data %>%
  group_by(username, ano) %>%  
  summarise(n = n(),
            engagement = sum (engage))
users$mean_engagement <- users$engagement/users$n
head(users)

#bootstrap analise
boot_eng <- users[,c(2,5)] %>%
  group_by(ano) %>%  
  group_map(~ smean.cl.boot(., conf.int = .95, B = 5000, na.rm = TRUE)) %>%
  bind_rows()
boot_eng$ano <- seq(2011,2020,1)
boot_eng

#plot
plot <- ggplot(boot_eng, aes(x = ano, y = Mean))
plot <- plot + geom_line() + geom_point()
plot <- plot + geom_line(aes(y = Lower), linetype = "dashed")
plot <- plot + geom_line(aes(y = Upper), linetype = "dashed")
plot <- plot + xlab("Year") + ylab("Mean engagement")
plot

