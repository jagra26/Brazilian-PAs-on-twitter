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
for directory in glob.glob(var.path + "2*"): # for each year, generate a cloud
    print(directory)
    if path.isdir(directory):
        df = pd.read_csv(glob.glob(directory + "/2*.csv")[0])
        #print(df.head())
        text = " ".join(str(review) for review in df.text)
        text_comp += text # update the general text
        name = directory.split("/")
        #print(name)
        create_cloud(directory, name[1], text)
create_cloud(var.path, "cloud", text_comp) # generate a general cloud
