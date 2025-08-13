import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

with open('used_car_price_model_v2.pkl', 'rb') as f:
    model = pickle.load(f)

app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array([data['features']])
    prediction = model.predict(features)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(port=5000, debug=True)