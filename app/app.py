import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import joblib
import helpers.weather_for_model as weather
import pandas as pd
import json

app = Flask(__name__)
model = joblib.load('model.z')

def create_stations_json():
    df = pd.read_json("../utils/stations.json")
    df = df[df['stationShortCodeCategory'] >= 0]
    df = df[['stationName',"stationShortCodeCategory"]].drop_duplicates()
    df.set_index('stationName',inplace=True)
    return df.to_dict()['stationShortCodeCategory']

stations = create_stations_json()

with open('../utils/lines.json', 'r') as f:
    lines = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', stations=stations, lines=lines)

@app.route('/predict',methods=['POST'])
def predict():

    inputs = [int(x) for x in request.form.values()]
    select_station = request.form.get('station')
    select_station = int(select_station)
    select_line = request.form.get('lineID')
    select_line = int(select_line)

    print(inputs)
    weatherPrediction = weather.give_prediction(inputs[2], inputs[3], inputs[4])
    print(weatherPrediction)  # 'rain', 'celcius', 'windGustSpeed', 'windSpeed'
    inputs.extend(weatherPrediction)
    inputs = [select_line] + inputs[1:1] + [select_station] + inputs[2:]  
    features = [np.array(inputs)]
    print("feat ", features)
    prediction = model.predict(features)
    res = int(prediction[0])

    return render_template('index.html', prediction_minutes='Delay {} minute(s)'.format(res), stations=stations, lines=lines)


if __name__ == "__main__":
    app.run(debug=True)
