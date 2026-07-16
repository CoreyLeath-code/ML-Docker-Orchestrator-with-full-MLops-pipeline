"""Model backends with a reproducible local default."""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Protocol

from .config import settings

log = logging.getLogger(__name__)
FEATURES = ("f1", "f2", "f3")


class Predictor(Protocol):
    def predict(self, records: list[dict[str, float]]) -> list[float]: ...


class DeterministicPredictor:
    """Reference model matching the synthetic training data's generating function."""

    def predict(self, records: list[dict[str, float]]) -> list[float]:
        return [
            2.0 * row["f1"] - row["f2"] + 0.5 * row["f3"]
            for row in records
        ]


class RegistryPredictor:
    def __init__(self) -> None:
        try:
            import mlflow
        except ImportError as exc:
            raise RuntimeError(
                "registry backend requires the optional mlflow dependency"
            ) from exc
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        uri = f"models:/{settings.model_name}@{settings.model_alias}"
        log.info("loading_registry_model", extra={"model_uri": uri})
        self._model = mlflow.pyfunc.load_model(uri)

    def predict(self, records: list[dict[str, float]]) -> list[float]:
        import pandas as pd

        return [float(value) for value in self._model.predict(pd.DataFrame(records))]


@lru_cache(maxsize=1)
def load_model() -> Predictor:
    if settings.model_backend == "registry":
        return RegistryPredictor()
    return DeterministicPredictor()


def predict(features: list[dict[str, float]]) -> list[dict[str, float]]:
    outputs = load_model().predict(features)
    return [{"prediction": float(value)} for value in outputs]
