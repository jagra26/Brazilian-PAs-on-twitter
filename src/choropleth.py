import folium
import pandas as pd
import time
from opencage.geocoder import OpenCageGeocode
from alive_progress import alive_bar
import variables as var
geocoder = OpenCageGeocode(var.opencage_key)

def choropleth_map(map, geojson, name, data, columns, key_on, legend_name,
    fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2):
    folium.Choropleth(
    geo_data=geojson,
    name=name,
    data=data,
    columns=columns,
    key_on=key_on,
    fill_color=fill_color,
    fill_opacity=fill_opacity,
    line_opacity=line_opacity,
    legend_name=legend_name,
    nan_fill_color="#F0F0F0"
    ).add_to(map)
    return map
def get_keys(df, countries, countriesID, states, statesID, iso, errors):
    with alive_bar(len(df)) as bar:
        for index in df.index:
            try:
                '''if index == 10:
                    break #test line'''
                lat = df.latitude[index]
                lon = df.longitude[index]
                quant = df.quantidade[index]
                #get country code and state
                address = geocoder.reverse_geocode(lat, lon)[0].get("components")
                #print(address)
                country_code = address.get('country_code')
                #print(country_code.upper())
                state = address.get('state')
                print(state)
                #convert alpha-2 to alpha-3
                iso_index = iso.index
                cond = iso["alpha-2"] == country_code.upper()
                alpha_3 = iso["alpha-3"][iso_index[cond]].values[0]
                print(alpha_3)
                #save quantities
                if countries.get(alpha_3) == None:
                    countries.update({alpha_3 : int(quant)})
                    countriesID.update({alpha_3 : str(df.ID[index])})
                else:
                    countries.update({alpha_3 : int(quant + countries.get(alpha_3))})
                    countriesID.update({alpha_3 : countriesID.get(alpha_3)+"/"+str(df.ID[index])})
                if alpha_3 == "BRA":
                    if state == None:
                        errors.update({df.ID[index] : "None"})      
                    elif states.get(state) == None:
                        states.update({state : int(quant)})
                        statesID.update({state : str(df.ID[index])})
                    else:
                        states.update({state : int(quant + states.get(state))})
                        statesID.update({state : statesID.get(state)+"/"+str(df.ID[index])})
                time.sleep(0.05)
                bar()
            except Exception as e:
                errors.update({df.ID[index] : str(e)})
                print(e)
                #break
    return
'''df = pd.read_excel("resources/coordenadas sumarizadas_lat e long.xlsx")
iso = pd.read_csv("resources/ISO-3166.csv")
countries = {}
countriesID = {}
states = {}
statesID = {}
errors = {}
print(df.head())

#convert coordinates in state and country
get_keys(df, countries, countriesID, states, statesID, iso, errors)
#define dataframes
countriesDF = pd.DataFrame.from_dict(countries, orient = 'index', columns = ['Quantity'])
countriesDF = countriesDF.reset_index()
countriesDF = countriesDF.rename(columns={'index':'Country'})
print(countriesDF.head())
statesDF = pd.DataFrame.from_dict(states, orient = 'index', columns = ['Quantity'])
statesDF = statesDF.reset_index()
statesDF = statesDF.rename(columns={'index':'State'})
print(statesDF.head())
#define dataframes
countriesIDDF = pd.DataFrame.from_dict(countriesID, orient = 'index', columns = ['ID'])
countriesIDDF = countriesIDDF.reset_index()
countriesIDDF = countriesIDDF.rename(columns={'index':'Country'})
print(countriesIDDF.head())
statesIDDF = pd.DataFrame.from_dict(statesID, orient = 'index', columns = ['ID'])
statesIDDF = statesIDDF.reset_index()
statesIDDF = statesIDDF.rename(columns={'index':'State'})
print(statesIDDF.head())
errorsDF = pd.DataFrame.from_dict(errors, orient = 'index', columns = ['Error'])
#save dataframes in files
countriesDF = countriesDF.merge(countriesIDDF, how='inner', on='Country')
statesDF = statesDF.merge(statesIDDF, how='inner', on='State')
print(countriesDF.head())
print(statesDF.head())
print("saving xlsx")
countriesDF.to_excel("resources/countriesDF.xlsx")
statesDF.to_excel("resources/statesDF.xlsx")
errorsDF.to_excel("resources/errorsDF.xlsx")
#state map'''
print("saving maps")
statesDF = pd.read_excel("resources/statesDF_vs carol.xlsx")
countriesDF = pd.read_excel("resources/countriesDF_carol.xlsx")
print(statesDF.head())
print(countriesDF.head())
m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)

state_geo = f'resources/brazil_geo.json'

m = choropleth_map(m, state_geo, 'choropleth_state', statesDF,
    ['State', 'Quantity'], 'properties.name', 'Number of Tweets per state')
m.save(var.path + "maps/choropleth_state.html")
#country map
m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
state_geo = f'resources/countries.geojson'
m = choropleth_map(m, state_geo, 'choropleth_country', countriesDF,
    ['Country', 'Quantity'], 'properties.ISO_A3', 'Number of Tweets per country', fill_color = "YlOrBr")
countries = pd.read_json("countries.geojson")
for i in countries['features']:
   if i['properties']['ADMIN'] == 'Brazil':
    country = i
    break
style_function = lambda x: {'fillColor': '#006600', 
                            'color':'#000000', 
                            'fillOpacity': 0.5, 
                            'weight': 0.1}
folium.GeoJson(country,
   name = 'Brazil', style_function=style_function).add_to(m)
folium.LayerControl().add_to(m)
m.save(var.path + "maps/choropleth_country.html")

print("done")
