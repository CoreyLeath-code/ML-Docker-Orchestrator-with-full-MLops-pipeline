from orchestrator.config import settings


def test_settings_defaults():
    assert settings.app_name
    assert settings.mlflow_tracking_uri
    assert settings.model_name
    assert settings.model_stage
