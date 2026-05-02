import logging
from functools import lru_cache
from typing import Any

import mlflow
import pandas as pd

from .config import settings

log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def load_model():
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    # Loads model from MLflow Model Registry stage (Production by default)
    model_uri = f"models:/{settings.model_name}/{settings.model_stage}"
    log.info("Loading model from MLflow", extra={"model_uri": model_uri})
    return mlflow.pyfunc.load_model(model_uri)


def predict(features: list[dict[str, Any]]) -> list[dict[str, Any]]:
    model = load_model()
    df = pd.DataFrame(features)
    preds = model.predict(df)
    # Normalize outputs into JSONable response
    return [{"prediction": float(p)} for p in preds]
