import glob
import pandas as pd

trains_data = pd.read_csv("clean/trains.csv", dtype={"commercialTrack": str}) 

path =r'data_weather'

def get_df(fn, area):
    filenames = glob.glob(path + fn)
    dfs = []
    for filename in filenames:
        dfs.append(pd.read_csv(filename))

    data = pd.concat(dfs, ignore_index=True)
    data['weather_area'] = area
    return data

data_helsinkivantaa = get_df("/hki-vantaa/*.csv", 1)
data_espoo = get_df("/espoo/*.csv", 2)
data_kirkkonummi = get_df("/kirkkonummi/*csv", 3)
data_lahti = get_df("/lahti/*csv", 4)
data_hameenlinna = get_df("/hameenlinna/*csv", 5)
data_tampere = get_df("/tampere/*csv", 6)
data_hyvinkaa = get_df("/hyvinkaa/*csv", 7)
data_lahti = get_df("/lahti/*csv", 8)

frames = [data_helsinkivantaa, data_espoo, data_kirkkonummi, data_lahti, data_hameenlinna, data_tampere, data_hyvinkaa, data_lahti]
weather_data = pd.concat(frames)

weather_data = weather_data.rename(columns = {'Vuosi': 'year', 'Kk': 'month', 'Pv': 'day', 'Klo': 'hour',
'Aikavyöhyke':'timezone', 'Sateen intensiteetti (mm/h)':'rain', 'Lumensyvyys (cm)':'snowDepth', 'Ilman lämpötila (degC)':'celcius',
 'Näkyvyys (m)':'visibility', 'Puuskanopeus (m/s)':'windGustSpeed', 'Tuulen nopeus (m/s)':'windSpeed'}, inplace = False)

weather_data["hour"] = weather_data["hour"].astype(str).str.replace(":00","").astype(int)

df = pd.merge(trains_data, weather_data, on= ['year', 'month', 'day', 'hour', 'weather_area'], how='left')

df.to_csv(r'trains_and_weather.csv', index = False)

