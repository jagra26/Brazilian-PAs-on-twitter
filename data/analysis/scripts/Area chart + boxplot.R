##################
# Assessing Brazilian protected areas through social media: insights from 10 years of public interest and engagement
# Updated 01/08/2023
# R 4.1.1 
##################


#Libraries
library(ggplot2)
library(dplyr)
library(viridis)
library(hrbrthemes)
library(plotly)


### AREA CHART

#import dataset

data_PAs <- read_excel("C:/Users/data_PAs.xlsx")
View(data_PAs)

# summarise  

volume_vs_engagement_vs_users <- data_PAs %>% 
  group_by(year) %>% 
  summarise(
    total_likes = sum(like_count, na.rm = TRUE),
    total_retweets = sum(retweet_count, na.rm = TRUE),
    n_of_posts = n(),
    qtd_users = n_distinct(username)
  ) %>% view()

#export_excel

install.packages("writexl")
library("writexl")

write_xlsx(volume_vs_engajamento_vs_usuarios, "C:\\Users\volume_vs_engagement.xlsx")

# Create data 

Year <- seq(2011,2020)

N_of_posts <- c(32241,
       43106,
       44426,
       51382,
       50097,
       45130,
       35109,
       29848,
       39256,
       31913)

Engagement <- c(7013,
                7460,
                11791,
                25030,
                29912,
                47187,
                101005,
                150534,
                535184,
                802305)

N_of_users <- c(14157,
                16712,
                19936,
                20642,
                18734,
                17709,
                15480,
                14714,
                20621,
                16534)


#plot 

p <- plot_ly(x = ~Year, y = ~N_of_posts, name = 'Volume of posts', type="scatter", mode='lines+markers', fill = "tozeroy", fillcolor = 'rgba(168, 216, 234, 1)')
p <- add_trace(p, x =Year, y = ~Engagement, name = 'Engagement', type="scatter", mode='lines+markers', fill = "tozeroy", fillcolor = 'rgba(255, 212, 96, 0.3)')
p <- add_trace(p, x =Year, y = ~N_of_users, name = 'N of users', type="scatter", mode='lines+markers', fill = "tozeroy", fillcolor = 'rgba(57,186,28, 0.3)')
p <- p %>% layout(legend = list(orientation = 'h', x = 0.8, y = 1))
p <- p %>% layout(font=list(size=12))
p

# save the widget
library(htmlwidgets)
saveWidget(p, file=paste0( getwd(), "/HtmlWidget/plotlyAreachart.html"))


### BOXPLOT

## year vs likes

library(dplyr)
library(tidyverse) 
library(readxl)

df_PAs <- read_excel("datas/df_PAS.xlsx")
View(df_PAs)

#changing class

df_caracter <- df_PAs %>% 
  mutate(year = as.character(year))

class(df_caracter$year)

#### colour plot

df_caracter %>% 
  ggplot() +
  scale_y_continuous(limits = c(0,11)) +
  geom_boxplot(
    aes(x = year, y = log(like_count), fill = year, alpha=0.9), 
    show.legend = FALSE
  ) + 
  scale_fill_manual(values = c("#000000", "#000000", "#000000", "#99FF66", "#66CC66", "#009900", "#66CCFF", "#3399CC", "#FF9900", "#FF6600")) +
  xlab("Year") + 
  ylab("Volume of likes") +
  theme_minimal()

#Save boxplot
ggsave("boxplot likes vs year.png", dpi = 300)
ggsave("boxplot likes vs year.pdf", dpi = 300)

#### boxplot one colour

df_caracter %>% 
  ggplot() +
  scale_y_continuous(limits = c(0,11)) +
  geom_boxplot(
    aes(x = year, y = log(like_count), fill = year, alpha=0.8), 
    show.legend = FALSE
  ) + 
  scale_fill_manual(values = c("#CCCCCC", "#CCCCCC", "#CCCCCC", "#CCCCCC", "#CCCCCC", "#CCCCCC", "#CCCCCC", "#CCCCCC", "#CCCCCC", "#CCCCCC")) +
  xlab("Year") + 
  ylab("Volume of likes") +
  theme_minimal()

#save boxplot

ggsave("boxplot likes vs year.png", dpi = 300)
ggsave("boxplot likes vs year.pdf", dpi = 300)

#References

citation("dplyr")
#Hadley Wickham, Romain François, Lionel Henry and Kirill Müller (2021). dplyr: A Grammar of Data Manipulation. R package version 1.0.7. https://CRAN.R-project.org/package=dplyr

citation("ggplot2")
# H. Wickham. ggplot2: Elegant Graphics for Data Analysis. Springer-Verlag New York, 2016.

citation("plotly")
#C. Sievert. Interactive Web-Based Data Visualization with R, plotly, and shiny. Chapman and Hall/CRC Florida, 2020.
