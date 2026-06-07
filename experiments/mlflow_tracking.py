# experiments/mlflow_tracking.py

import mlflow
from orchestrator.config import settings


def configure_mlflow():
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)


def log_experiment(params: dict, metrics: dict):
    with mlflow.start_run():
        for key, value in params.items():
            mlflow.log_param(key, value)
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
