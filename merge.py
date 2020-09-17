import glob
import pandas as pd

trains_data = pd.read_csv("trains.csv", dtype={"commercialTrack": str}) 
path =r'data_weather'
filenames = glob.glob(path + "/*.csv")
dfs = []
for filename in filenames:
    dfs.append(pd.read_csv(filename))

weather_data = pd.concat(dfs, ignore_index=True)

weather_data = weather_data.rename(columns = {'Vuosi': 'year', 'Kk': 'month', 'Pv': 'day', 'Klo': 'hour',
'Aikavyöhyke':'timezone', 'Sateen intensiteetti (mm/h)':'rain', 'Lumensyvyys (cm)':'snowDepth', 'Ilman lämpötila (degC)':'celcius',
 'Näkyvyys (m)':'visibility', 'Puuskanopeus (m/s)':'windGustSpeed', 'Tuulen nopeus (m/s)':'windSpeed'}, inplace = False)

weather_data["hour"] = weather_data["hour"].astype(str).str.replace(":00","").astype(int)

df = pd.merge(trains_data, weather_data, on= ['year', 'month', 'day', 'hour'], how='left')

df.to_csv(r'trains_and_weather.csv', index = False)
