from fastapi.testclient import TestClient

from orchestrator import api

client = TestClient(api.app)


def test_predict_endpoint_sanitizes_model_failures(monkeypatch):
    def unavailable(_):
        raise RuntimeError("mlflow registry token must not reach callers")

    monkeypatch.setattr(api, "predict", unavailable)

    response = client.post("/predict", json={"records": [{"f1": 1, "f2": 2, "f3": 3}]})

    assert response.status_code == 503
    assert response.json() == {"detail": "Prediction service unavailable"}
    assert "token" not in response.text


def test_predict_endpoint_rejects_empty_batches(monkeypatch):
    monkeypatch.setattr(api, "predict", lambda _: [])

    response = client.post("/predict", json={"records": []})

    assert response.status_code == 422
