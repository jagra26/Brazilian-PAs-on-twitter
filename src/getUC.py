import numpy as np
import pandas as pd
from os import path
import variables as var
import glob 
import os
import re
from alive_progress import alive_bar


def getUC(file, name, keylist, ucComplete):
	df = pd.read_csv(file, lineterminator='\n')
	db = {}
	with alive_bar(len(df.index)) as bar:
		for tweet in df.index:
			for UC in keylist:
				if " "+UC.casefold() in str(df['text'][tweet]).casefold():
					try:
						'''wordsUC = UC.casefold().split(" ")
						wordsTweet = re.sub(r'[^\w\s]', ' ', df['text'][tweet].casefold()).split(" ")
						index = wordsTweet.index(wordsUC[-1])
						location = UC
						for i in range (1,5):
							if index+i <= len(wordsTweet)-1:
								location += " "
								location += wordsTweet[index + i]
						#print(location)'''
						index = keylist.index(UC)
						location = ucComplete[index]
						db.update({df['id'][tweet] : location})
						bar()
						break
					except Exception as e:
						print(e)
	UCs = pd.DataFrame.from_dict(db, orient='index')
	UCs.to_csv(name+".csv")

'''listUC = ["Unidade de conservação" , "Area protegida" , 
"Parque Nacional" , "Parque estadual" , "Parque natural municipal" , 
"Parque municipal" , "Estação ecológica" , "Reserva biológica" , 
"Monumento natural" , "Refúgio da vida silvestre" , "Reserva extrativista" , 
"Área de proteção ambiental" , "Floresta nacional" , "Floresta estadual" , 
"Floresta municipal" , "Reserva de desenvolvimento sustentável" , 
"Área de relevante interesse", "Reserva Particular do Patrimônio Natural"]
allUCs = pd.read_csv("cnuc_2020_2-semestre.csv", error_bad_lines=False, sep=';')
allUCsList = allUCs['Nome da UC'].tolist()'''
keyword = pd.read_csv("LISTAS-DE-UCS_NOME-PROPRIO.csv", error_bad_lines=False, sep=',')
keywordList = keyword['palavra chave'].tolist()
UCList = keyword['nome da uc'].tolist()

for directory in glob.glob(var.path + "2*"):
	print(directory)
	if len(glob.glob(directory + "/*_limpo*.csv")) != 0:
		file = glob.glob(directory + "/*_limpo*.csv")[0]
		getUC(file, directory + "/clearkeyUC", keywordList, UCList)
	

