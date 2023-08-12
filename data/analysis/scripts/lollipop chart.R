##################
# Assessing Brazilian protected areas through social media: insights from 10 years of public interest and engagement
# Updated 24/09/2021
# R 4.1.1 
##################


#-------- WHICH PAs HAVE BEEN MOST TALKED ABOUT ON TWITTER IN THE LAST 10 YEARS? 

library(ggplot2)
library(dplyr)
library(ggplot2)
library(forcats)
library(tidyverse)
library(ggalt)
library(tidyquant)

## dataset

PAs <- c("Parque Nacional do Iguaçu", "Parque Nacional da Tijuca", "Parque Nacional do Itatiaia", "Parque Nacional da Chapada dos Veadeiros", "Parque Nacional do Lençóis Maranhenses", 
              "Parque Nacional da Serra dos Órgãos", "Parque Nacional da Serra da Capivara", "Parque Nacional de Brasília", 
              "Parque Estadual de Vila Velha", "Parque Nacional da Serra da Canastra")
posts <- c(21746,
             9507,
             8280,
             4330,
             4197,
             4108,
             3529,
             3143,
             3116,
             2648)

top10_pas <- data.frame(x = PAs, y = posts)

top_PAS_desc <- data.frame(PAS, posts)

##--- Horizontal version

top_PAS_desc  %>%
  mutate(
    PAS = forcats::fct_reorder(PAS, posts) # decreasing
  ) %>% ggplot(aes(x= PAS, y= posts)) + 
  geom_point(aes(color= PAS), size=4, alpha=0.6) +
  geom_segment(aes(x= PAS, xend=PAS, y=0, yend= posts, color = PAS)) +
    theme_light() +
    scale_colour_viridis_d() +
  coord_flip() +
  theme(
    panel.grid.major.y = element_blank(),
    panel.border = element_blank(),
    axis.ticks.y = element_blank(),
    legend.position = "none"
  ) +
    labs(
    x = "Protected areas",
    y = " N of posts",
    title = "The 30 most tweeted protected areas",
    subtitle = "2011-2020")

ggsave("top 30 tweeted protected areas.png", dpi = 300)


# WHICH PAS HAVE HAD THE MOST ENGAGEMENT?

top_engaged  %>%
  arrange(group) %>%
  mutate(
   protected_areas = forcats::fct_reorder(protected_areas, soma_engajamento) 
  ) %>%  
  ggplot(aes(x= protected_areas, y= soma_engajamento, fill=group)) + 
  geom_point(aes(color= group), size=5, alpha=0.6) +
  geom_segment(aes(x= protected_areas, xend=protected_areas, y=0, yend= soma_engajamento, color = group)) +
  theme_light() +
  coord_flip() +
  theme(
    panel.grid.major.y = element_blank(),
    panel.border = element_blank(),
    axis.ticks.y = element_blank(),
    legend.position= "right"
  ) +
  labs(
    x = "Protected areas",
    y = " N of posts",
    title = "The 30 most engaged protected areas",
    subtitle = "2011-2020",
    legend=TRUE)

ggsave("v2_top 30 engaged tweeted protected areas.png", dpi = 600)
ggsave("v2_top 30 engaged tweeted protected areas.pdf", dpi = 600)


#References

citation("dplyr")
#Hadley Wickham, Romain François, Lionel Henry and Kirill Müller (2021). dplyr: A Grammar of Data Manipulation. R package version 1.0.7. https://CRAN.R-project.org/package=dplyr

citation("ggplot2")
# H. Wickham. ggplot2: Elegant Graphics for Data Analysis. Springer-Verlag New York, 2016.

citation("forcats")
#Hadley Wickham (2021). forcats: Tools for Working with Categorical Variables (Factors). R package version 0.5.1. https://CRAN.R-project.org/package=forcats



