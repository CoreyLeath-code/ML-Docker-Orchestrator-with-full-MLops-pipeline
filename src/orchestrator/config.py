# src/orchestrator/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ML Docker Orchestrator"
    app_env: str = "development"

    model_path: str = "models/model.pkl"
    data_path: str = "data/"
    mlflow_tracking_uri: str = "http://localhost:5000"
    model_name: str = "orchestrator-model"
    model_stage: str = "Production"

    log_level: str = "INFO"
    metrics_enabled: bool = True

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
