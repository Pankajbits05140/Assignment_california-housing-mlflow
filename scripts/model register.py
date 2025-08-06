import mlflow
from mlflow.tracking import MlflowClient

# Initialize the MLflow client
client = MlflowClient()

# Search for runs within an experiment
runs = client.search_runs(
    experiment_ids=["476160720550869773"],  # Replace "0" with your experiment ID
    order_by=["metrics.rmse ASC"],  # Sort by RMSE in ascending order
    run_view_type=mlflow.entities.ViewType.ACTIVE_ONLY
)

# Get the best run (the first one after sorting)
best_run = runs[0]
best_run_id = best_run.info.run_id

# Define the model URI. "model" is the default artifact path.
model_uri = f"runs:/{best_run_id}/model"
model_name = "MyBestModel" # Choose a descriptive name for your registered model

# Register the model
result = mlflow.register_model(model_uri, model_name)

print(f"Registered model '{result.name}' as version {result.version}")