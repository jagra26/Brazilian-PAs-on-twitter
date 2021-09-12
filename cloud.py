# Start with loading all necessary libraries
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import variables as var
import tkinter
import glob 
import matplotlib.pyplot as plt
import os
def create_cloud(path, name, text):
    wordcloud = WordCloud(stopwords=var.stopwords, background_color="white").generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    wordcloud.to_file(os.path.join(path, name + ".png"))
    plt.show()

text_comp = " "
for directory in glob.glob(var.path + "*"):
    print(directory)
    if path.isdir(directory):
        df = pd.read_csv(glob.glob(directory + "/*.csv")[0])
        #print(df.head())
        text = " ".join(str(review) for review in df.text)
        text_comp += text
        name = directory.split("/")
        #print(name)
        create_cloud(directory, name[1], text)
create_cloud("./", "cloud", text_comp)
"""
df = pd.read_csv(var.path + "2020-01-01_2020-12-31/2020-01-01_2020-12-31.csv")
# Looking at first 5 rows of the dataset
print(df.head())
#text = df.text[0]
text = " ".join(str(review) for review in df.text)
#print(text)
"""
