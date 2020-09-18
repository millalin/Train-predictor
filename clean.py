import os
import glob
import pandas as pd
import datetime

# Location of data directory
data_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
json_files = glob.glob(os.path.join(data_folder, "raw", "*.json"))
extra_columns = ["actualTime", "cancelled", "commercialTrack", "differenceInMinutes",
				 "scheduledTime", "stationShortCode", "trainStopping", "categoryCodeId", "categoryCode",
				 "detailedCategoryCode", "detailedCategoryCodeId", "year", "month", "day", "hour", "direction"]

dfs = []
for json_file in json_files:
	df = pd.read_json(json_file)
	df = df[(df["commuterLineID"] != "") & (df["trainCategory"].str.contains("Commuter"))]
	df = df[["trainCategory", "commuterLineID", "timeTableRows"]]
	df = pd.concat([df, pd.DataFrame(index=df.index, columns=extra_columns)], axis=1)

# Set row values from timeTableRows to created extra columns
	for i, row in df.iterrows():
		direction = 0 if row['timeTableRows'][-1]["stationShortCode"] == "HKI" else 1
		for k in row["timeTableRows"]:
			[k.pop(key, None) for key in["stationUICCode", "countryCode", "type", "commercialStop", "liveEstimateTime", "estimateSource", "unknownDelay", "trainReady"]]

			date = datetime.datetime.strptime(k["scheduledTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
			row["month"] = date.month
			row["day"] = date.day
			row["hour"] = date.hour
			row["year"] = date.year
			row["direction"] = direction

			if k["causes"]:
				[k["causes"][0].pop(key, None) for key in ["thirdCategoryId", "thirdCategoryCodeId"]]
				for key in k["causes"][0]:
					row[key] = k["causes"][0][key]
			k.pop("causes", None)
			for key in k:
				row[key] = k[key]
	df = df.drop(["actualTime", "scheduledTime", "timeTableRows"], axis=1)
	dfs.append(df)

df = pd.concat(dfs)

# clean up NaNs from certain columns, also remove N and V trains and rows with empty commercialTrack
filtered_cols = ["cancelled", "commercialTrack", "commuterLineID"]
df = df[(df[filtered_cols].notnull().all(1)) & (df["commuterLineID"] != "N") & (df["commuterLineID"] != "V") &  (df["commercialTrack"] != "")]

destination=os.path.join(data_folder, "clean", "trains.csv")
df.to_csv(destination, index = False)
