##################
# Assessing Brazilian protected areas through social media: insights from 10 years of public interest and engagement
# Updated 27/07/2023
# R 4.1.1 
##################

#libraries 
library(readxl)
library(ggplot2)
library (ggalt)

# import dataset
users <- data_PAs_users <- read_excel("C:/Users/data_users.xlsx")
View(users)

###scatter plot GGPLOT2

#median analisys

median(log(users$N)) #yline
median(users$N)

median(log(users$`mean engagement`)) #xline
median(users$`mean engagement`)

##plot

ggplot(users, aes(x=log10(`mean engagement` + 1), y=log10(N))) +
  geom_point(aes(col=verified, size= `mean engagement`)) +
  geom_hline(yintercept = 1) + 
  geom_vline(xintercept = 0) + 
  labs (title = "Users",
        y= "No. of tweets",
        x= "Likes + Retweets (Engagement)",
        subtitle = "Posts vs Engagement") +
  theme_minimal()

ggsave("users vs posts.png", dpi = 600)


### Correlation non-parametric (n of tweets vs mean engagement)

#### SPEARMAN
resultado_cor <- cor.test(users$N, users$`mean engagement`, method = "spearman", alternative="two.sided")

#print result
print(resultado_cor)

#### KENDALL
resultado_cor <- cor.test(users$N, users$`mean engagement`, method = "kendall", alternative="two.sided")

# print result
print(resultado_cor)


#References
citation ("ggalt")
#Bob Rudis, Ben Bolker and Jan Schulz (2017). ggalt: Extra Coordinate Systems, 'Geoms', Statistical Transformations, Scales and Fonts for 'ggplot2'. R package version 0.4.0.https://CRAN.R-project.org/package=ggalt






