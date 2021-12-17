from flask import Flask
from flask import request
import json
import numpy as np

app = Flask(__name__)
from mlflow_server import MLFlowServer

mfs = MLFlowServer()

@app.route("/predict", methods=['GET'])
def predict():
    return {'prediction': mfs.predict_fn(request.json.get('data')).tolist()}

if __name__ == '__main__':
    app.run(port=8080, debug=True)