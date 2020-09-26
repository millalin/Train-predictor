import os
import requests
from fmiopendata.wfs import download_stored_query
import datetime
import json
import pandas as pd

# dir_path = os.path.dirname(os.path.realpath(__file__))
# base_url = "http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::multipointcoverage&place=helsinki&"
# destination_folder = os.path.join(dir_path, "we_pred", "raw")

# r = requests.get(base_url, destination_folder)

# Retrieve the latest hour of data from a bounding box


end_time = datetime.datetime.utcnow()
start_time = end_time - datetime.timedelta(hours=5)
# Convert times to properly formatted strings
start_time = start_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T12:00:00Z
end_time = end_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T13:00:00Z
hki_vantaa_lat_lon = 60.3267, 24.95675


# 'Helsinki': {'fmisid': 658225, 'latitude': 60.16952, 'longitude': 24.93545}
# 'Helsinki-Vantaa airport': {'fmisid': 16000063, 'latitude': 60.3267, 'longitude': 24.95675},

# obs_hki_vantaa = download_stored_query("fmi::forecast::hirlam::surface::point::multipointcoverage",
#                                        args=["starttime=" + start_time,
#                                              "endtime=" + end_time, "latlon=60.3267,24.95675"])

# obs_hki_vantaa = download_stored_query("fmi::observations::weather::multipointcoverage",
#                                        args=["place=Helsinki",
#                                              "starttime=" + start_time, "endtime=" + end_time])
place = 'Helsinki'
obs_hki = download_stored_query("fmi::observations::weather::multipointcoverage",
                                       args=["place=" + place,
                                             "starttime=" + start_time, "endtime=" + end_time])                                             

print(obs_hki.location_metadata)
print(obs_hki.data)
time_of_day = list(obs_hki.data.keys())[0]
rain = obs_hki.data[time_of_day][place]['Precipitation intensity']['value']

df = pd.DataFrame(columns=['year', 'month',  'day',  'hour', 'timezone',
                           'rain', 'snowDepth', 'celcius', 'visibility', 'windGustSpeed', 'windSpeed'])
print(df)
#df.loc[[0], ['year', 'month',  'day',  'hour', 'timezone', 'rain', 'snowDepth', 'celcius', 'visibility', 'windGustSpeed', 'windSpeed']] = time_of_day.year, time_of_day.month, time_of_day.day, time_of_day.hour, 'UTC', rain,
