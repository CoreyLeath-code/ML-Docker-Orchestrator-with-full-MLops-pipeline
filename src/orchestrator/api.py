import logging
import time
from typing import Any

from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field

from .config import settings
from .logging_config import configure_logging
from .metrics import LATENCY, REQUESTS, metrics_response
from .model import predict

configure_logging(settings.log_level)
log = logging.getLogger("orchestrator")

app = FastAPI(title="ML Docker Orchestrator", version="0.1.0")


class PredictRequest(BaseModel):
    records: list[dict[str, Any]] = Field(
        ..., min_length=1, max_length=1_000, description="List of feature dicts"
    )


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.app_env}


@app.get("/metrics")
def metrics():
    if not settings.metrics_enabled:
        return Response(content="metrics disabled", status_code=404)
    content, status, headers = metrics_response()
    return Response(content=content, status_code=status, headers=headers)


@app.post("/predict")
def predict_endpoint(payload: PredictRequest, response: Response):
    start = time.time()
    try:
        out = predict(payload.records)
        response.status_code = 200
        return {"predictions": out}
    except Exception:
        log.exception("prediction_failed")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"detail": "Prediction service unavailable"}
    finally:
        dur = time.time() - start
        path = "/predict"
        method = "POST"
        REQUESTS.labels(path=path, method=method, status=str(response.status_code)).inc()
        LATENCY.labels(path=path, method=method).observe(dur)
