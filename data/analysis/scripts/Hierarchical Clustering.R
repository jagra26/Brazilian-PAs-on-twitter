##################
# Assessing Brazilian protected areas through social media: insights from 10 years of public interest and engagement
# Updated 25/02/2022
# R 4.1.1 
##################

memory.limit()
memory.limit(size=12500)

# Read the necessary packages
library(tm)
library(wordcloud)
library(topicmodels)
library(tidytext)
library(tidyverse)
library(quanteda)
library(readxl)
library(ldatuning)
library(xlsx)
library(widyr)
library(ggraph)
library(igraph)
library(factoextra)
library(cluster)
library(dendextend)
library(writexl)

# Load the data
df <- read_excel("C:/Users/data_text_id.xlsx")
head(df)

# Get the text column
text <- as.data.frame(df$text)

# Filter out links, special characters and resulting multiple white spaces
text_trim_url <- data.frame(text = apply(text, 1, function(x) gsub("http.*"," ", x)))
head(text_trim_url)
text_trim_spchr <- data.frame(text = apply(text_trim_url, 1, function(x) str_replace_all(x, "[^[:alnum:]]", " ")))
head(text_trim_spchr)
text_trim <- data.frame(doc_id = seq(1, nrow(text_trim_spchr), 1),
                        text = apply(text_trim_spchr, 1, str_squish))
head(text_trim)
beepr::beep(sound = 2) #sinal de termino da analise

# Remove unneeded objects from memory
rm(text_trim_url, text_trim_spchr, text)

# Create the corpus
text_corpus <- VCorpus(DataframeSource(text_trim))
writeLines(as.character(text_corpus[[1]]))
beepr::beep(sound = 2)

#### Clean the corpus
# Convert all letters to small case
text_corpus_clean <- tm_map(text_corpus, content_transformer(tolower))

# Remove unneeded objects to clear memory
rm(text_corpus, text_trim)

# Clean stop words
text_corpus_clean <- tm_map(text_corpus_clean, removeWords, stopwords("portuguese"))   

# Remove numbers
text_corpus_clean <- tm_map(text_corpus_clean, removeNumbers)

# Remove punctuation
text_corpus_clean <- tm_map(text_corpus_clean, removePunctuation)

# Remove whitespace
text_corpus_clean <- tm_map(text_corpus_clean, stripWhitespace)

# Create the DTM to check word frequencies
text_dtm <- DocumentTermMatrix(text_corpus_clean)
text_dtm
beepr::beep(sound = 2)

# Create list of very common terms and remove them
verycommon <- findFreqTerms(text_dtm, lowfreq = 21000)
verycommon
common <- findFreqTerms(text_dtm, lowfreq = 4000)
common
keepOnlyWords <- content_transformer(function(x, words) {
  regmatches(x, 
             gregexpr(paste0("\\b(",  paste(words, collapse = "\\b|\\b"), "\\b)"), x)
             , invert = T) <- " "
  x
})
text_corpus_filter <- tm_map(text_corpus_clean, keepOnlyWords, common)   
text_corpus_filter <- tm_map(text_corpus_filter, stripWhitespace)


# Create the DTM to check word frequencies
text_dtm <- DocumentTermMatrix(text_corpus_filter)
text_dtm
inspect(text_dtm)


# Remove empty rows
ui = unique(text_dtm$i)
text_dtm.new = text_dtm[ui,]
text_dtm.new
inspect(text_dtm.new)


# Partitioning around medioids
text_mat.new <- as.matrix(text_dtm.new)
text_df.new <- data.frame(text_mat.new)
text_df.new$doc <- seq(1, nrow(text_df.new),1)
beepr::beep(sound=2)

#remove objects from memory
rm(text_dtm,text_corpus_clean, text_corpus_filter, text_mat.new, text_dtm.new, common, keepOnlyWords, ui, verycommon,df )

# continue...Partitioning around medioids
text_df.new <- gather(text_df.new, word, count, ambiental:voce)
head(text_df.new)

text_df <- text_df.new[which(text_df.new$count>0),]
head(text_df)

#sumarize words from df
text_df_sumarized <- text_df %>% 
  group_by(word) %>% 
  summarise(quantidade = n())

#save table
setwd("C:/Users//Cluster/")
write_xlsx(text_df_sumarized, path = "text_df_sumarized.xlsx")

# Calculate correlation
word.phi <- text_df %>%
  group_by(word) %>%
  filter(n() >= 4000 & n() <=21000) %>%
  pairwise_cor(word, doc, count, sort = T)
word.phi

# Convert object to matrix
text.mat <- spread(word.phi, item1, correlation)
head(text.mat)

#save matrix
write_xlsx(text.mat, path = "text.matrix.xlsx")

make_matrix <- function(df,rownames = NULL){
  my_matrix <-  as.matrix(df)
  if(!is.null(rownames))
    rownames(my_matrix) = rownames
  my_matrix
}

dist.mat <- make_matrix(select(text.mat,-item2),
                        pull(text.mat,item2))
diag(dist.mat) <- 1
head(dist.mat)

#save matrix
write_xlsx(dist.mat, path = "dist.matrix.xlsx")

dist <- as.dist(sqrt(2*(1 - dist.mat)))
head(dist)

#create clusters
test <- hclust(dist, method = "complete")
plot(color_branches(test, k=5))
k<-5


# dendrogram with colours
fviz_dend(test, k,
          cex = 0.5,
          k_colors = c('#7fc97f','#8c510a','#386cb0',
                       '#f0027f','#bf5b17'),
          color_labels_by_k = TRUE, 
          rect = TRUE
)

# new presentation cluster format
grp <- cutree(test, k = 5)
head(grp, n = 5)

fviz_cluster(list(data = dist, cluster = grp),
             
             palette = c('#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00'),
             ellipse.type = "convex", # Concentration ellipse
             repel = TRUE, # Avoid label overplotting (slow)
             show.clust.cent = FALSE, ggtheme = theme_minimal())


#set.seed(8)
#km.res <- kmeans(dist, 5, nstart = 15)
#View(km.res)
#print(km.res)

#number of clusters
clusters <- read_excel("text_df_sumarized_clusters.xlsx")
clusters_grouped <- clusters %>% 
  group_by(cluster,word) %>% 
  summarise(quantidade = n())

#References

citation("cluster")
# Maechler, M., Rousseeuw, P., Struyf, A., Hubert, M., Hornik, K.(2021).  cluster: Cluster Analysis Basics and Extensions. R package version 2.1.2.

citation("factoextra")
#Alboukadel Kassambara and Fabian Mundt (2020). factoextra: Extract and Visualize the Results of Multivariate Data Analyses. R package version 1.0.7. https://CRAN.R-project.org/package=factoextra
