import folium
import pandas as pd
import time
from opencage.geocoder import OpenCageGeocode
from alive_progress import alive_bar
key = 'b6aec148db9542058e8caa8fbafdf579'
geocoder = OpenCageGeocode(key)

def choropleth_map(map, geojson, name, data, columns, key_on, legend_name,
    fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2):
    folium.Choropleth(
    geo_data=geojson,
    name=name,
    data=data,
    columns=columns,
    key_on=key_on,
    fill_color=fill_color,
    fill_opacity=fill_opacity,
    line_opacity=line_opacity,
    legend_name=legend_name
    ).add_to(map)
    return map
def get_keys(df, countries, states, iso):
    with alive_bar(len(df)) as bar:
        for index in df.index:
            try:
                '''if index == 10:
                    break''' #test line
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
                else:
                    countries.update({alpha_3 : int(quant + countries.get(alpha_3))})
                if alpha_3 == "BRA": 
                    if states.get(state) == None:
                        states.update({state : int(quant)})
                    else:
                        states.update({state : int(quant + states.get(state))})
                    
                time.sleep(1)
                bar()
            except Exception as e:
                print(e)
                #break
    return
df = pd.read_excel("coordenadas sumarizadas_lat e long.xlsx")
iso = pd.read_csv("ISO-3166.csv")
countries = {}
states = {}
print(df.head())

#convert coordinates in state and country
get_keys(df, countries, states, iso)
#define dataframes
countriesDF = pd.DataFrame.from_dict(countries, orient = 'index', columns = ['Quantity'])
countriesDF = countriesDF.reset_index()
countriesDF = countriesDF.rename(columns={'index':'Country'})
print(countriesDF.head())
statesDF = pd.DataFrame.from_dict(states, orient = 'index', columns = ['Quantity'])
statesDF = statesDF.reset_index()
statesDF = statesDF.rename(columns={'index':'State'})
print(statesDF.head())
#save dataframes in files
print("saving xlsx")
countriesDF.to_excel("countriesDF.xlsx")
statesDF.to_excel("statesDF.xlsx")
#state map
print("saving maps")
m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
state_geo = f'brazil_geo.json'
m = choropleth_map(m, state_geo, 'choropleth_state', statesDF,
    ['State', 'Quantity'], 'properties.name', 'Quantidade')
m.save("choropleth_state.html")
#country map
m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
state_geo = f'countries.geojson'
m = choropleth_map(m, state_geo, 'choropleth_country', countriesDF,
    ['Country', 'Quantity'], 'properties.ISO_A3', 'Quantidade')
m.save("choropleth_country.html")

print("done")
# TODO: map
"""
    {'place_id': 199470353, 
    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright', 
    'osm_type': 'way', 
    'osm_id': 493370539, 
    'lat': '-3.10357925', 
    'lon': '-60.02494495100177', 
    'display_name': 'Pátio Goumert, Avenida Djalma Batista, São Geraldo, Manaus, Região Geográfica Imediata de Manaus, Região Geográfica Intermediária de Manaus, Amazonas, Região Norte, 69000-000, Brasil', 
    'address': {
    'shop': 'Pátio Goumert', 
    'road': 'Avenida Djalma Batista', 
    'suburb': 'São Geraldo', 
    'city_district': 'Manaus', 
    'city': 'Manaus', 
    'municipality': 'Região Geográfica Imediata de Manaus', 
    'state_district': 'Região Geográfica Intermediária de Manaus', 
    'state': 'Amazonas', 
    'region': 'Região Norte', 
    'postcode': '69000-000', 
    'country': 'Brasil', 
    'country_code': 'br'}, 
    'boundingbox': ['-3.103883', '-3.1032688', '-60.0252912', '-60.0246018']}
    """