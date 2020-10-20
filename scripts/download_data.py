import os
import datetime
import zipfile
import glob
import requests

# Directory this script is at
base_url = "https://rata.digitraffic.fi/api/v1/trains/dumps/digitraffic-rata-trains-{}.zip"

destination_folder = os.path.join("../data/raw")
end_date = datetime.date(2020, 9, 1)

for year in range(2017, 2021):
	for month in range(1, 13):
		dt = datetime.date(year, month, 1)
		if dt >= end_date:
			break
		r = requests.get(base_url.format(dt), destination_folder)
		with open(f"{destination_folder}/{dt}.zip", "wb") as f:
			f.write(r.content)

# Unzip downloaded files, then delete zips
zips = glob.glob(f"{destination_folder}/*.zip")

for zipf in zips:
	with zipfile.ZipFile(zipf, 'r') as zip_ref:
 	   zip_ref.extractall(destination_folder)
 	   os.remove(zipf)
