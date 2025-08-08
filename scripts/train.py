# scripts/train.py

import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

df = pd.read_csv("data/raw/california_housing.csv")
X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "LinearRegression": LinearRegression(),
    "DecisionTree": DecisionTreeRegressor(max_depth=5, random_state=42)
}

mlflow.set_experiment("california-housing")

for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)

        mlflow.log_param("model_type", model_name)
        mlflow.log_metric("mse", mse)
        mlflow.sklearn.log_model(model, "model")

        print(f"{model_name} MSE: {mse:.4f}")
        mlflow.sklearn.save_model(model, "model/best_model")