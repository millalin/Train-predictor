import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import helpers.weather_for_model as weather

app = Flask(__name__)
model = pickle.load(open('modeltrain.pkl', 'rb'))
# or joblib (?)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    inputs = [int(x) for x in request.form.values()]
    print(inputs)
    weatherPrediction = weather.give_prediction(inputs[1], inputs[2], inputs[3])
    print(weatherPrediction)  # 'rain', 'celcius', 'windGustSpeed', 'windSpeed'
    inputs.extend(weatherPrediction)
    features = [np.array(inputs)]
    prediction = model.predict(features)

    res = prediction[0]

    return render_template('index.html', prediction_minutes='Delay {} minute(s)'.format(res))

if __name__ == "__main__":
    app.run(debug=True)
