from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from orchestrator.api import app
from orchestrator.config import Settings
from orchestrator.model import DeterministicPredictor, load_model, predict

client = TestClient(app)


def test_health_readiness_and_metrics():
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/live").status_code == 200
    assert client.get("/ready").json()["model_backend"] == "deterministic"
    assert "http_requests_total" in client.get("/metrics").text


def test_prediction_is_deterministic():
    response = client.post(
        "/predict",
        json={"records": [{"f1": 1, "f2": 2, "f3": 3}]},
    )
    assert response.status_code == 200
    assert response.json() == {"predictions": [{"prediction": 1.5}]}


@pytest.mark.parametrize(
    "payload",
    [
        {"records": []},
        {"records": [{"f1": 1, "f2": 2}]},
        {"records": [{"f1": 1, "f2": 2, "f3": 3, "extra": 4}]},
        {"records": [{"f1": "NaN", "f2": 2, "f3": 3}]},
    ],
)
def test_invalid_contracts(payload):
    assert client.post("/predict", json=payload).status_code == 422


def test_batch_limit(monkeypatch):
    monkeypatch.setattr("orchestrator.api.settings.max_batch_size", 1)
    response = client.post(
        "/predict",
        json={"records": [{"f1": 1, "f2": 2, "f3": 3}] * 2},
    )
    assert response.status_code == 413


def test_sanitized_model_failure():
    with patch("orchestrator.api.predict", side_effect=RuntimeError("secret detail")):
        response = client.post(
            "/predict", json={"records": [{"f1": 1, "f2": 2, "f3": 3}]}
        )
    assert response.status_code == 503
    assert "secret detail" not in response.text


def test_readiness_failure():
    with patch("orchestrator.api.load_model", side_effect=RuntimeError("offline")):
        assert client.get("/ready").status_code == 503


def test_metrics_can_be_disabled(monkeypatch):
    monkeypatch.setattr("orchestrator.api.settings.metrics_enabled", False)
    assert client.get("/metrics").status_code == 404


def test_model_helpers_and_cache():
    model = DeterministicPredictor()
    assert model.predict([{"f1": 2, "f2": 1, "f3": 4}]) == [5.0]
    assert predict([{"f1": 0, "f2": 0, "f3": 0}]) == [{"prediction": 0.0}]
    assert load_model() is load_model()


def test_settings_validation():
    settings = Settings(app_env="production", max_batch_size=10)
    assert settings.model_backend == "deterministic"
    with pytest.raises(ValueError):
        Settings(max_batch_size=0)
