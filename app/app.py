import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import joblib
import helpers.weather_for_model as weather

app = Flask(__name__)
model = joblib.load('model.z')

@app.route('/')
def home():
    return render_template('index.html')

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

    return render_template('index.html', prediction_minutes='Delay {} minute(s)'.format(res))

if __name__ == "__main__":
    app.run(debug=True)
