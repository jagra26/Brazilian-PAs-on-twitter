import pandas as pd
from opencage.geocoder import OpenCageGeocode
from alive_progress import alive_bar
import variables as var
import time

geocoder = OpenCageGeocode(var.opencage_key)

df = pd.read_excel("resources/need coordinates 2021-2022.xlsx")
df_new = pd.DataFrame(columns=["Adress", "Lat", "Long"])
print(df.head())

with alive_bar(len(df)) as bar:
    for index in df.index:
        try:
            results = geocoder.geocode(df.full_name[index], no_annotations='1')
            df_new.loc[len(df_new)] = [df.full_name[index],
                                       results[0]['geometry']['lat'], results[0]['geometry']['lng']]
            bar()
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)

df_new.to_excel("results/coord.xlsx")
