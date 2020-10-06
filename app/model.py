import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('../data/merged/trains_and_weather.csv', low_memory=False)

dataset = dataset.astype({'commuterLineID': 'category', 'stationShortCode': 'category'})
categoryToNumeric = dataset.select_dtypes(['category']).columns
dataset[categoryToNumeric] = dataset[categoryToNumeric].apply(lambda x: x.cat.codes)

# For now selecting commuterLineID, stationShortCode, month, day, hour, direction, rain, celcius, windGustSpeed, windSpeed
X = dataset.iloc[0:100000,lambda df: [0,1,6,7,8,13,14,15,16,17]]
y = dataset.iloc[0:100000, 3]

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    train_size=0.80, test_size=0.20, random_state=66)

rf = RandomForestClassifier(max_depth=12, random_state=66, n_estimators=100)
rf.fit(X_train, y_train)
y_predtrain_rf = rf.predict(X_train)

joblib.dump(rf, 'model.z')

# Testing after building model

model2 = joblib.load('model.z')
print(model2.predict([[1,8, 6, 2, 22, 1, 0.0, 14.42, 3.77, 1.55]]))

