import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('modeltrain.pkl', 'rb'))
# or joblib (?)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    inputs = [int(x) for x in request.form.values()]
    features = [np.array(inputs)]
    # weather still missing
    prediction = model.predict(features)

    res = prediction[0]

    return render_template('index.html', prediction_minutes='Delay {} minute(s)'.format(res))

if __name__ == "__main__":
    app.run(debug=True)
