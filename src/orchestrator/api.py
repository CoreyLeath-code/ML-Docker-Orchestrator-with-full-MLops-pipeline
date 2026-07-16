"""Observable, validated inference API."""

import logging
import math
import time
from typing import Annotated

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import settings
from .logging_config import configure_logging
from .metrics import LATENCY, REQUESTS, metrics_response
from .model import FEATURES, load_model, predict

configure_logging(settings.log_level)
log = logging.getLogger("orchestrator")
app = FastAPI(title=settings.app_name, version="1.0.0")


class FeatureRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    f1: float
    f2: float
    f3: float

    @field_validator("f1", "f2", "f3")
    @classmethod
    def finite(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("features must be finite")
        return value


class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    records: Annotated[list[FeatureRecord], Field(min_length=1)]


@app.get("/health")
@app.get("/live")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    try:
        load_model()
    except Exception as exc:
        log.warning("model_not_ready", extra={"backend": settings.model_backend})
        raise HTTPException(status_code=503, detail="model unavailable") from exc
    return {"status": "ready", "model_backend": settings.model_backend}


@app.get("/metrics")
def metrics() -> Response:
    if not settings.metrics_enabled:
        raise HTTPException(status_code=404, detail="metrics disabled")
    content, status, headers = metrics_response()
    return Response(content=content, status_code=status, headers=headers)


@app.post("/predict")
def predict_endpoint(payload: PredictRequest) -> dict:
    if len(payload.records) > settings.max_batch_size:
        raise HTTPException(status_code=413, detail="batch exceeds configured limit")
    started = time.perf_counter()
    status = 200
    try:
        records = [
            {feature: getattr(record, feature) for feature in FEATURES}
            for record in payload.records
        ]
        return {"predictions": predict(records)}
    except Exception as exc:
        status = 503
        log.exception("prediction_failed")
        raise HTTPException(status_code=503, detail="model unavailable") from exc
    finally:
        REQUESTS.labels(path="/predict", method="POST", status=str(status)).inc()
        LATENCY.labels(path="/predict", method="POST").observe(
            time.perf_counter() - started
        )
