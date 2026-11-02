"""
Centralized configuration for Fanous backend.

Reads from environment variables (prefixed with FANOUS_) and .env files.
Use this as the single source of truth for all configurable values.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import StrEnum


class ModelMode(StrEnum):
    moondream_hf = "hf"
    moondream_direct = "moon"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FANOUS_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    debug: bool = True

    #  Model
    model_mode: ModelMode = ModelMode.moondream_direct
    moondream_api_key: str | None = None
    hf_token: str | None = None

    # Server
    host: str = "0.0.0.0"
    port: int = 8001

    # Inference 
    caption_timeout: int = 120
    max_file_size_mb: int = 50


# Singleton instance btw
settings = Settings()
