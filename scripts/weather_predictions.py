import os
import requests
from fmiopendata.wfs import download_stored_query
import datetime
import json
import pandas as pd

# Retriew forecast for seven locations, max prediction + 54 h, save to csv-file

now = datetime.datetime.utcnow()
end_time = now + datetime.timedelta(hours=36)
start_time = end_time - datetime.timedelta(hours=1)
# Convert times to properly formatted strings
start_time = start_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T12:00:00Z
end_time = end_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T13:00:00Z


place_index = ['Helsinki', 'Espoo', 'Kirkkonummi', 'Lahti',
               'Hämeenlinna', 'Tampere', 'Hyvinkää', 'Kouvola']
places = ["latlon=60.3267,24.95675", "latlon=60.17797,24.78743", "latlon=60.29128,24.56782",
          "latlon=60.97465,25.6202", "latlon=61,24.49", "latlon=61.50124,23.76478", "latlon=60.6,24.8", "latlon=60.7,26.81"]

rows = []

for place in places:

    obs = download_stored_query("fmi::forecast::hirlam::surface::point::multipointcoverage",
                                args=["starttime=" + start_time,
                                      "endtime=" + end_time, place])

    print(obs.location_metadata)
    print(obs.data)
    time_of_day = max(obs.data.keys())
    print('timestamp', time_of_day)

    weather_station = list(obs.data[time_of_day].keys())[0]
    print(weather_station)

    data = obs.data[time_of_day][weather_station]
    rain = data['Precipitation amount 1 hour']['value']
    celcius = data['Air temperature']['value']
    windGustSpeed = data['Wind gust']['value']
    windSpeed = data['Wind speed']['value']

    row = [time_of_day.year, time_of_day.month, time_of_day.day, time_of_day.hour,
           rain,  celcius, windGustSpeed, windSpeed]
    rows.append(row)

df = pd.DataFrame(rows, columns=['year', 'month',  'day',  'hour',
                                 'rain', 'celcius', 'windGustSpeed', 'windSpeed'], index=place_index)

print('time now', now)
print('prediction time range:', start_time, end_time)
print(df)
df.to_csv(r'../data_weather_predictions/latest_weather_observations.csv', index=True)
