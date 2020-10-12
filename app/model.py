import matplotlib.pyplot as plt
import pandas as pd
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import json


def update_stations_json(df):
    with open("../utils/stations.json", 'r', encoding="utf-8") as f:
        stations = json.load(f)
        # Temporarily store category code to new column
        df['stationShortCodeCategory'] = df['stationShortCode'].astype("category").cat.codes
        station_cat = df[['stationShortCode',"stationShortCodeCategory"]].drop_duplicates()
        for station in stations:
            category = station_cat[station_cat["stationShortCode"] == station["stationShortCode"]]["stationShortCodeCategory"].values
            if len(category) == 0:
                station["stationShortCodeCategory"] = -1
                continue
            station["stationShortCodeCategory"] = int(category[0])
    with open("../utils/stations.json", "w", encoding="utf-8") as f:
        json.dump(stations, f, ensure_ascii=False)


dataset = pd.read_csv('../data/merged/trains_and_weather.csv', low_memory=False)

update_stations_json(dataset)
dataset["stationShortCode"] = dataset['stationShortCodeCategory']
train = dataset['commuterLineID'].drop_duplicates()
commuterLineID = dataset['commuterLineID'].astype("category").cat.codes
dataset['commuterLineID'] = commuterLineID
lineID = commuterLineID.drop_duplicates()
lines = dict(zip( lineID, train ))

with open("../utils/lines.json", "w") as f:  
    json.dump(lines, f) 


# For now selecting commuterLineID, stationShortCode, month, day, hour, direction, weekday, rain, celcius, windGustSpeed, windSpeed
X = dataset.iloc[0:1000000,lambda df: [0,1,6,7,8,13,14,15,16,17, 18]]
y = dataset.iloc[0:1000000, 3]

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    train_size=0.80, test_size=0.20, random_state=66)

rf = RandomForestClassifier(max_depth=12, random_state=66, n_estimators=100)
rf.fit(X_train, y_train)
y_predtrain_rf = rf.predict(X_train)

joblib.dump(rf, 'model.z')

# Testing after building model

model2 = joblib.load('model.z')
score = rf.score(X_test, y_test)
print(score)

