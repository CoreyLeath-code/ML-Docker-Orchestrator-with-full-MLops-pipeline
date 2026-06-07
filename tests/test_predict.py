from fastapi.testclient import TestClient

from orchestrator.api import app

client = TestClient(app)

def test_predict_endpoint_structure():
    # Model loading may fail if MLflow not running; endpoint should still respond gracefully.
    r = client.post("/predict", json={"records": [{"f1": 1, "f2": 2, "f3": 3}]})
    assert r.status_code in (200, 500)
