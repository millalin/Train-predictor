import os
import requests
from fmiopendata.wfs import download_stored_query
import datetime
import json
import pandas as pd

# Retrieve the latest observations for several locations, save to csv-file

end_time = datetime.datetime.utcnow()
start_time = end_time - datetime.timedelta(hours=5)
# Convert times to properly formatted strings
start_time = start_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T12:00:00Z
end_time = end_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T13:00:00Z

places = ['Kumpula,Helsinki', 'Tapiola,Espoo',
          'Kirkkonummi', 'Lahti', 'Tampere']
place_index = ['Helsinki', 'Espoo', 'Kirkkonummi', 'Lahti', 'Tampere']
# Hämeenlinna and Hyvinkää queries not implemented, the places used in merge are:
# places = ['Kumpula,Helsinki', 'Espoo', 'Kirkkonummi', 'Lahti', 'Hämeenlinna, 'Tampere', 'Hyvinkää', 'Lahti']
rows = []
for place in places:
    obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                                args=["place=" + place,
                                      "starttime=" + start_time, "endtime=" + end_time])
    # print(obs.location_metadata)
    # print(obs.data)
    time_of_day = max(obs.data.keys())
    print('timestamp', time_of_day)

    weather_station = list(obs.data[time_of_day].keys())[0]
    print(weather_station)

    data = obs.data[time_of_day][weather_station]
    rain = data['Precipitation intensity']['value']
    snowDepth = data['Snow depth']['value']
    celcius = data['Air temperature']['value']
    visibility = data['Horizontal visibility']['value']
    windGustSpeed = data['Gust speed']['value']
    windSpeed = data['Wind speed']['value']

    row = [time_of_day.year, time_of_day.month, time_of_day.day, time_of_day.hour,
           'UTC', rain, snowDepth, celcius, visibility, windGustSpeed, windSpeed]
    rows.append(row)

df = pd.DataFrame(rows, columns=['year', 'month',  'day',  'hour', 'timezone',
                                 'rain', 'snowDepth', 'celcius', 'visibility', 'windGustSpeed', 'windSpeed'], index=place_index)
print(df)
df.to_csv(r'data-we-pred/latest_weather_observations.csv', index=True)
