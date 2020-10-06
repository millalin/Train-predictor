import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import joblib
import helpers.weather_for_model as weather
import pandas as pd

app = Flask(__name__)
model = joblib.load('model.z')

def create_stations_json():
    df = pd.read_json("../utils/stations.json")
    df = df[df['stationShortCodeCategory'] >= 0]
    df = df[['stationName',"stationShortCodeCategory"]].drop_duplicates()
    df.set_index('stationName',inplace=True)
    return df.to_dict()['stationShortCodeCategory']

stations = create_stations_json()


@app.route('/')
def home():
    return render_template('index.html', stations=stations)

@app.route('/predict',methods=['POST'])
def predict():

    inputs = [int(x) for x in request.form.values()]
    print(inputs)
    weatherPrediction = weather.give_prediction(inputs[2], inputs[3], inputs[4])
    print(weatherPrediction)  # 'rain', 'celcius', 'windGustSpeed', 'windSpeed'
    inputs.extend(weatherPrediction)
    features = [np.array(inputs)]
    prediction = model.predict(features)

    res = int(prediction[0])

    return render_template('index.html', prediction_minutes='Delay {} minute(s)'.format(res), stations=stations)

if __name__ == "__main__":
    app.run(debug=True)
