"""Validated environment configuration."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ML Docker Orchestrator"
    app_env: Literal["development", "test", "staging", "production"] = "development"
    model_backend: Literal["deterministic", "registry"] = "deterministic"
    mlflow_tracking_uri: str = "http://localhost:5000"
    model_name: str = "orchestrator-model"
    model_alias: str = "champion"
    log_level: str = "INFO"
    metrics_enabled: bool = True
    max_batch_size: int = Field(default=1000, ge=1, le=10_000)

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
