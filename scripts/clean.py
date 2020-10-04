import os
import glob
import pandas as pd
import datetime
import json

# Location of data directory
data_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
json_files = glob.glob(os.path.join(data_folder, "raw", "*.json"))

commuter_line_ids = ["Y","U","L","E","A","P","I","K","R","T","D","Z"]

used_columns = ["commuterLineID", "stationShortCode", "commercialTrack", "differenceInMinutes", 
 				"weather_area", "year", "month", "day", "hour", "categoryCode", "categoryCodeId",
 				"detailedCategoryCode", "detailedCategoryCodeId", "direction"]


with open("../utils/weather_stations.json") as f:
	weather_stations = json.load(f)


def get_cause_category(key, causes):
	return None if len(causes) == 0 or key not in causes[0] else causes[0][key]


dfs = []
for json_file in json_files:
	df = pd.read_json(json_file)
	df = df[df['trainCategory'] == "Commuter"]
	df['direction'] = df['timeTableRows'].apply(lambda x: 1 if x[0]["stationShortCode"] == "HKI" else 0)
	df = df.explode("timeTableRows")
	df = df[df['commuterLineID'].isin(commuter_line_ids)]
	sub_df = pd.json_normalize(df["timeTableRows"])

	df = df.reset_index()
	sub_df = sub_df.reset_index()

	df = pd.concat([df, sub_df], axis=1)
	df = df[df["stationShortCode"].notna()]
	df = df[(df["commercialTrack"].notna())]
	df = df[df["commercialStop"] == True]
	df = df[df["trainStopping"] == True]
	df = df[df["type"] == "DEPARTURE"]

	df['weather_area'] = df['stationShortCode'].apply(lambda x: 0 if x not in weather_stations else weather_stations[x])
	df["year"] = df["scheduledTime"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").year)
	df["month"] = df["scheduledTime"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").month)
	df["day"] = df["scheduledTime"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").day)
	df["hour"] = df["scheduledTime"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ").hour)

	df["categoryCode"] = df["causes"].apply(lambda x: get_cause_category("categoryCode", x))
	df["categoryCodeId"] = df["causes"].apply(lambda x: get_cause_category("categoryCodeId", x))
	df["detailedCategoryCode"] = df["causes"].apply(lambda x: get_cause_category("detailedCategoryCode", x))
	df["detailedCategoryCodeId"] = df["causes"].apply(lambda x: get_cause_category("detailedCategoryCodeId", x))

	df = df[used_columns]
	df = df[df["differenceInMinutes"].notna()]
	dfs.append(df)

df = pd.concat(dfs)
destination=os.path.join(data_folder, "clean", "trains.csv")
df.to_csv(destination, index = False)
