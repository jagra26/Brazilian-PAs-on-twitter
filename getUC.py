import numpy as np
import pandas as pd
from os import path
import variables as var
import glob 
import os
import re
from alive_progress import alive_bar


def getUC(file, name, listUC):
	df = pd.read_csv(file, lineterminator='\n')
	db = {}
	with alive_bar(len(df.index)) as bar:
		for tweet in df.index:
			for UC in listUC:
				if UC.casefold() in str(df['text'][tweet]).casefold():
					try:
						wordsUC = UC.casefold().split(" ")
						wordsTweet = re.sub(r'[^\w\s]', ' ', df['text'][tweet].casefold()).split(" ")
						index = wordsTweet.index(wordsUC[-1])
						location = UC
						for i in range (1,5):
							if index+i <= len(wordsTweet)-1:
								location += " "
								location += wordsTweet[index + i]
						#print(location)
						db.update({df['id'][tweet] : location})
						bar()
						break
					except Exception as e:
						print(e)
	UCs = pd.DataFrame.from_dict(db, orient='index')
	UCs.to_csv(name+".csv")

listUC = ["Unidade de conservação" , "Area protegida" , 
"Parque Nacional" , "Parque estadual" , "Parque natural municipal" , 
"Parque municipal" , "Estação ecológica" , "Reserva biológica" , 
"Monumento natural" , "Refúgio da vida silvestre" , "Reserva extrativista" , 
"Área de proteção ambiental" , "Floresta nacional" , "Floresta estadual" , 
"Floresta municipal" , "Reserva de desenvolvimento sustentável" , 
"Área de relevante interesse", "Reserva Particular do Patrimônio Natural"]
for directory in glob.glob(var.path + "2*"):
    print(directory)
    if len(glob.glob(directory + "/*_limpo*.csv")) != 0:
	    file = glob.glob(directory + "/*_limpo*.csv")[0]
	    getUC(file, directory + "/UC", listUC)
	

"""tweet = "Acabou de publicar uma foto em Parque Nacional da Chapada dos Guimarães https://t.co/CJN2U1ANpG"
uc = "Parque Nacional"
if uc in tweet:
	words = tweet.split(" ")
	index = words.index("Nacional")
	print(uc, words[index+1], words[index+2], words[index+3], words[index+4])"""