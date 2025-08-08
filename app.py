from flask import Flask, request, jsonify, send_from_directory
import mlflow.sklearn
import pandas as pd
import traceback
import os
import sqlite3
from datetime import datetime
from flask_cors import CORS
import logging

# ------------------ Logging Setup ------------------
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ SQLite Setup -------------------
DB_FILE = "logs.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    input_data TEXT,
    prediction TEXT
)
""")
conn.commit()

# ------------------ Flask App ----------------------
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
        # Get input
        data = request.get_json(force=True)
        input_df = pd.DataFrame([data])

        # Predict
        prediction = model.predict(input_df)
        pred_value = float(prediction[0])

        # Log to file
        logging.info(f"Request: {data}, Prediction: {pred_value}")

        # Log to SQLite
        cursor.execute(
            "INSERT INTO predictions (timestamp, input_data, prediction) VALUES (?, ?, ?)",
            (datetime.utcnow().isoformat(), str(data), str(pred_value))
        )
        conn.commit()

        return jsonify({"prediction": pred_value})

    except Exception as e:
        logging.error(f"Error: {str(e)}, Trace: {traceback.format_exc()}")
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 400

@app.route("/metrics", methods=["GET"])
def metrics():
    cursor.execute("SELECT COUNT(*), AVG(CAST(prediction AS REAL)) FROM predictions")
    count, avg_pred = cursor.fetchone()
    return jsonify({
        "total_requests": count,
        "average_prediction": avg_pred if avg_pred is not None else 0
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)