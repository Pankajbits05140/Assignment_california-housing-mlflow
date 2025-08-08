from flask import Flask, request, jsonify, send_from_directory
import mlflow.sklearn
import pandas as pd
import traceback
import os
from flask_cors import CORS

app = Flask(__name__, static_folder="frontend")
CORS(app)

# Load model
model = mlflow.sklearn.load_model("model/best_model")

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)
        return jsonify({"prediction": float(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)