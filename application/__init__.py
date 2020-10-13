import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
from application.helpers import weather_for_model as weather
import pandas as pd
import json
import datetime
import os
import boto3

app = Flask(__name__, static_folder= os.path.join(os.path.dirname(os.path.realpath(__file__)), "static"))
model = joblib.load('application/model')
bucket = os.environ['S3_BUCKET']


def create_stations_json():
    df = pd.read_json("utils/stations.json")
    df = df[df['stationShortCodeCategory'] >= 0]
    df = df[['stationName',"stationShortCodeCategory"]].drop_duplicates()
    df.set_index('stationName',inplace=True)
    return df.to_dict()['stationShortCodeCategory']

stations = create_stations_json()

@app.route("/map_features")
def get_map_features():
    key = request.args.get("geojson")
    client = boto3.client("s3")
    resp = client.get_object(Bucket=bucket, Key=key)
    resp = resp['Body'].read().decode('utf-8')
    response = app.response_class(
        response=resp,
        mimetype='application/json'
    )
    return response



@app.route("/historical_data")
def historical_data():
    return render_template("map.html")

with open('utils/lines.json', 'r') as f:
    lines = json.load(f)

@app.route('/home')
def home():
    return render_template('index.html', stations=stations, lines=lines)

@app.route('/predict',methods=['POST'])
def predict():
    inputs = [int(x) for x in request.form.values()]
    year = datetime.datetime.now().year
    weekday = datetime.datetime(year=year, month=inputs[2], day=inputs[3]).weekday()
    select_station = request.form.get('station')
    select_station = int(select_station)
    select_line_str = request.form.get('lineID')
    select_line = int(select_line_str)

    print(inputs)
    weatherPrediction = weather.give_prediction(inputs[1], inputs[2], inputs[3], inputs[4])
    # convert weather predictions to int
    used_weather_values = list(map(int, weatherPrediction[0:4]))
    print(used_weather_values)  # rain, celcius, windGustSpeed, windSpeed
    inputs.append(weekday)
    inputs.extend(used_weather_values)
    inputs = [select_line] + inputs[1:1] + [select_station] + inputs[2:]  
    features = [np.array(inputs)]
    print("feat ", features)

    direction = ', train coming from Helsinki main station' if inputs[5] == 1 else ', train going towards Helsinki main station'
    prediction_info = f'Date and time: {weatherPrediction[6].strftime("%d/%m/%Y %H:%M")}, train {lines.get(select_line_str)}, station {weatherPrediction[4]}{direction}'
    weather_info = f'Weather prediction for {weatherPrediction[5]} weather station: rain amount: {weatherPrediction[0]} mm/h, temperature: {weatherPrediction[1]} ℃, wind gusts: {weatherPrediction[2]} m/s, wind speed: {weatherPrediction[3]} m/s'
    features_sum = np.sum(features)

    if np.isnan(features_sum):
        return render_template('index.html', prediction_minutes='Cannot get a prediction for this time', stations=stations, lines=lines, prediction_info=prediction_info, weather_info=weather_info)

    prediction = model.predict(features)
    res = int(prediction[0])
    res_explained= {0: '0', 1:'1-2', 2: 'over 3'}

    return render_template('index.html', prediction_minutes='Predicted train delay {} minute(s)'.format(res_explained.get(res)), stations=stations, lines=lines, prediction_info=prediction_info, weather_info=weather_info)

@app.route('/statistics', methods=['POST'])
def statistics():
    return render_template('statistics.html', stations=stations, lines=lines)
