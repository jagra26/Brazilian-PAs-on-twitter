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
import matplotlib.pyplot as plt
from IPython.display import HTML, display
import webbrowser

def get_coordinates(df, name):
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
	with alive_bar(len(cities)) as bar:
		for place in cities.full_name:
			try:
				print(place)
				point = geolocator.geocode(place).point
				pair = (round(point.latitude, 2), round(point.longitude, 2))
				if db.get(pair) is None:
					db.update({pair : 1})
				else:
					db[pair] += 1
				bar()
			except Exception as e:
				print(e)
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
	print(db)
def generate_map(file):
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
	m.save("map.html")
df = pd.read_csv("./results/2021-01-01_2021-07-31/2021-01-01_2021-07-31.csv")
print(df)
#get_coordinates(df, "test")
generate_map("test.csv")