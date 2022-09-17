import pandas as pd
import requests

df = pd.read_csv('resale_flat_prices.csv')

#Iterating through each row of the dataframe

df['unique_add'] = df['block'] + ' ' + df['street_name']
df = df[['unique_add']].drop_duplicates()

def latlon(sample_df_row):
  base_url = "https://developers.onemap.sg/"
  path= "/commonapi/search?searchVal={}&returnGeom={}&getAddrDetails={}".format(str(sample_df_row[0]),'Y','Y')
  result= requests.get(base_url+path)
  #   print(str(sample_df_row[0]))
  #   print(result.json())
  if result.json()['found'] >= 1:
    x, y=  result.json()['results'][0]['LONGITUDE'],result.json()['results'][0]['LATITUDE'] 
  else:
    print(result.json())
    x, y = 'NULL','NULL'
  return x,y


df.loc[:,'Lon'], df.loc[:,'Lat']= zip(*df['unique_add'].apply(latlon))
df.to_csv('unique_add_latlon.csv')

