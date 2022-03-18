from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="example app")
import numpy as np
import pandas as pd
from os import path
import variables as var
import glob 
import os
from alive_progress import alive_bar
import folium
import time

def get_coordinates(file, name): # function to get coordinates and the number of tweets of each coordinate
	df = pd.read_csv(file, lineterminator='\n')
	print(df.head())
	geotagged_df = df[~df.place_id.isnull()]
	coordinates_list = list(geotagged_df[~geotagged_df.coordinates.isnull()].coordinates)
	db = {}
	for i in range(len(coordinates_list)):
		coordinates_list[i] = coordinates_list[i][1:-1].split(", ")
		pair = (round(float(coordinates_list[i][1]), 2),
		 round(float(coordinates_list[i][0]), 2))
		if db.get(pair) is None:
			db.update({pair : 1})
		else:
			db[pair] += 1
	cities = geotagged_df[geotagged_df.coordinates.isnull()]
	changed_tweets = {}
	with alive_bar(len(cities)) as bar:
		for ind in cities.index:
			try:
				place = cities['full_name'][ind]
				print(place)
				point = geolocator.geocode(place).point
				pair = (round(point.latitude, 2), round(point.longitude, 2))
				tweet_id = cities['id'][ind]
				changed_tweets.update({tweet_id:'[' + str(point.longitude) + ', ' + str(point.latitude) + ']'})
				if db.get(pair) is None:
					db.update({pair : 1})
				else:
					db[pair] += 1
				bar()
			except Exception as e:
				print(e)
	print(changed_tweets)
	tweetsCoordinates = pd.DataFrame.from_dict(changed_tweets, orient='index')
	tweetsCoordinates.to_csv(name+'tweets.csv')
	lat = []
	long = []
	N = []
	for coordinates in db:
		lat.append(coordinates[0])
		long.append(coordinates[1])
		N.append(db[coordinates])
	data = {'lat' : lat, 'long' : long, 'N': N}
	coordinates = pd.DataFrame(data=data)
	coordinates.to_csv(name+".csv")
	#print(db)
def generate_map(file, out): # function to generate a map with a circle in each coordinate, the radius change conform the number of tweets
	m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
	data = pd.read_csv(file, dtype=str)
	for i in range(0,len(data)):
		folium.Circle(
		location=[data.iloc[i]['lat'], data.iloc[i]['long']],
		radius=float(data.iloc[i]['N'])*2000,
		color='crimson',
		fill=True,
		fill_color='crimson'
		).add_to(m)
	m.save(out)
def general_map(): # function to generate a general coordinates.csv 
	dic = {}
	for directory in glob.glob(var.path + "2*"):
		if path.isdir(directory):
			df = pd.read_csv((glob.glob(directory + "/coordinates.csv")[0]))
			for ind in df.index:
				pair = (df['lat'][ind], df['long'][ind])
				if dic.get(pair) is None:
						dic.update({pair : df['N'][ind]})
				else:
					dic[pair] += df['N'][ind]
	lat = []
	long = []
	N = []
	for coordinates in dic:
		lat.append(coordinates[0])
		long.append(coordinates[1])
		N.append(dic[coordinates])
	data = {'lat' : lat, 'long' : long, 'N': N}
	coordinates = pd.DataFrame(data=data)
	coordinates.to_csv("resources/coordinates.csv")

for directory in glob.glob(var.path + "2*"): # for each result directory 
	print(directory)
	if len(glob.glob(directory + "/*_limpo*.csv")) != 0:
		file = glob.glob(directory + "/*_limpo*.csv")[0]
		get_coordinates(file, directory + "/coordinates") # get coordinates
		generate_map(directory + "/coordinates.csv", directory + "/map.html") # generate map
		print("sleep for 10 seconds")
		time.sleep(10)

general_map()
generate_map("resources/coordinates.csv", var.path+"maps/general_map.html")