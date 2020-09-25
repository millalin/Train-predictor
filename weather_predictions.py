import os
import requests
from fmiopendata.wfs import download_stored_query
import datetime
import json

#dir_path = os.path.dirname(os.path.realpath(__file__))
#base_url = "http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::multipointcoverage&place=helsinki&"
#destination_folder = os.path.join(dir_path, "we_pred", "raw")

#r = requests.get(base_url, destination_folder)

# Retrieve the latest hour of data from a bounding box


end_time = datetime.datetime.utcnow()
start_time = end_time - datetime.timedelta(hours=1)
# Convert times to properly formatted strings
start_time = start_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T12:00:00Z
end_time = end_time.isoformat(timespec="seconds") + "Z"
# -> 2020-07-07T13:00:00Z

obs = download_stored_query("fmi::forecast::hirlam::surface::obsstations::multipointcoverage",
                            args=["bbox=18,55,35,75",
                                  "starttime=" + start_time,
                                  "endtime=" + end_time])
#obs.data.to_json('data_weather/weather_predictions.json', orient='records')
#json.dumps(obs.data)
print(obs.data)
