import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import json


def update_stations_json(df):
    with open("../utils/stations.json", 'r', encoding="utf-8") as f:
        stations = json.load(f)
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


dataset = pd.read_csv('../data/merged/trains_and_weather.csv')

update_stations_json(dataset)
dataset["stationShortCode"] = dataset['stationShortCodeCategory']


# For now selecting differenceinMinutes, month, day, hour, direction, rain, celcius, windGustSpeed, windSpeed
X = dataset.iloc[0:100000,lambda df: [1,6,7,8,13,14,15,16,17]]
y = dataset.iloc[0:100000, 3]

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    train_size=0.80, test_size=0.20, random_state=66)

rf3 = RandomForestClassifier(max_depth=12, random_state=66, n_estimators=100)
rf3.fit(X_train, y_train)
y_predtrain_rf3 = rf3.predict(X_train)

pickle.dump(rf3, open('modeltrain.pkl','wb'))

# Testing after building model
model = pickle.load(open('modeltrain.pkl','rb'))
print(model.predict([[8, 6, 2, 22, 1, 0.0, 14.42, 3.77, 1.55]]))
