"""Test configuration: set env vars so tests don't require external services."""

import os

# Use a local file-based MLflow store so tests never attempt a network connection
os.environ.setdefault("MLFLOW_TRACKING_URI", "file:///tmp/mlruns-test")
os.environ.setdefault("MODEL_NAME", "test-model")
os.environ.setdefault("MODEL_STAGE", "None")
