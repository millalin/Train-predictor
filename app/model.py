import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('../data/merged/trains_and_weather.csv')

dataset = dataset.astype({'stationShortCode': 'category'})
categoryToNumeric = dataset.select_dtypes(['category']).columns
dataset[categoryToNumeric] = dataset[categoryToNumeric].apply(lambda x: x.cat.codes)

# For now selecting differenceinMinutes, month, day, hour, direction
X = dataset.iloc[0:100000,lambda df: [1,6,7,8,13]]
y = dataset.iloc[0:100000, 3]

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    train_size=0.80, test_size=0.20, random_state=66)

rf3 = RandomForestClassifier(max_depth=12, random_state=66, n_estimators=100)
rf3.fit(X_train, y_train)
y_predtrain_rf3 = rf3.predict(X_train)

pickle.dump(rf3, open('modeltrain.pkl','wb'))

# Testing after building model
model = pickle.load(open('modeltrain.pkl','rb'))
print(model.predict([[5, 6, 2, 22, 1]]))