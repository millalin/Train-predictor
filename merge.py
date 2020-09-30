import glob
import pandas as pd

trains_data = pd.read_csv("data/clean/trains.csv", dtype={"commercialTrack": str})

path =r'data_weather'

def get_df(fn, area):
    filenames = glob.glob(path + fn)
    dfs = []
    for filename in filenames:
        dfs.append(pd.read_csv(filename))

    data = pd.concat(dfs, ignore_index=True)
    data['weather_area'] = area
    return data

def get_df_wind(fn):
    filenames = glob.glob(path + fn)
    dfs = []
    for filename in filenames:
        dfs.append(pd.read_csv(filename))

    data = pd.concat(dfs, ignore_index=True)
    return data

def get_one_file(fn):
    data = pd.read_csv(fn)
    return data

data_helsinkivantaa = get_df("/hki-vantaa/*.csv", 1)
data_espoo = get_df("/espoo/*.csv", 2)
data_kirkkonummi = get_df("/kirkkonummi/*.csv", 3)
data_tampere = get_df("/tampere/*.csv", 6)
data_hyvinkaa = get_df("/hyvinkaa/*.csv", 7)
data_kouvola = get_df("/kouvola/*.csv", 8)

data_wind_tre = get_df_wind("/wind/tre/*.csv")
data_wind_central = get_df_wind("/wind/central/*.csv")

del data_wind_central['Aikavyöhyke']
del data_wind_tre['Aikavyöhyke']

def wind(data1, data2):
    del data1['Tuulen nopeus (m/s)']
    del data1['Puuskanopeus (m/s)']
    del data1['Aikavyöhyke']

    data1 = pd.merge(data1, data2, on= ['Vuosi', 'Kk', 'Pv', 'Klo'], how='left')
    return data1

data_tampere = wind(data_tampere,data_wind_tre)
data_kouvola = wind(data_kouvola, data_wind_central)
data_hyvinkaa = wind(data_hyvinkaa, data_wind_central)

# Lahti missing wind values only from 2019 so getting those from different file with wind weather info from nearby area
data_lahti_wind19 = get_one_file("./data_weather/wind/central/wind_hlinna_kouv_lahti_hyv_2019.csv")
data_lahti_19 = get_one_file("./data_weather/lahti/weather_lahtiheinola-2019.csv")
data_lahti_1718 = get_one_file("./data_weather/lahti/weather_lahti_2017-2018.csv")
data_lahti_19 = wind(data_lahti_19,data_lahti_wind19)
data_lahti = pd.concat([data_lahti_19, data_lahti_1718])
data_lahti['weather_area'] = 4

# Hämeenlinna missing wind values only from 2019 so getting those from different file with wind weather info from nearby area
data_hameenlinna_wind19 = get_one_file("./data_weather/wind/central/wind_hlinna_kouv_lahti_hyv_2019.csv")
data_hameenlinna_19 = get_one_file("./data_weather/hameenlinna/weather_hameenlinna_2019.csv")
data_hameenlinna_1718 = get_one_file("./data_weather/hameenlinna/weather_hameenlinna2017-2018.csv")
data_hameenlinna_19 = wind(data_hameenlinna_19,data_hameenlinna_wind19)
data_hameenlinna = pd.concat([data_hameenlinna_19, data_hameenlinna_1718])
data_hameenlinna['weather_area'] = 5

frames = [data_helsinkivantaa, data_espoo, data_kirkkonummi, data_lahti, data_hameenlinna, data_tampere, data_hyvinkaa, data_kouvola]
weather_data = pd.concat(frames)

del weather_data['Aikavyöhyke']
weather_data = weather_data.rename(columns = {'Vuosi': 'year', 'Kk': 'month', 'Pv': 'day', 'Klo': 'hour',
'Sateen intensiteetti (mm/h)':'rain', 'Lumensyvyys (cm)':'snowDepth', 'Ilman lämpötila (degC)':'celcius',
'Näkyvyys (m)':'visibility', 'Puuskanopeus (m/s)':'windGustSpeed', 'Tuulen nopeus (m/s)':'windSpeed'}, inplace = False)

weather_data["hour"] = weather_data["hour"].astype(str).str.replace(":00","").astype(int)

df = pd.merge(trains_data, weather_data, on= ['year', 'month', 'day', 'hour', 'weather_area'], how='left')

df.to_csv(r'trains_and_weather.csv', index = False)

