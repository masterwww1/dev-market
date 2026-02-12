"""B2Bmarket backend configuration.

This module automatically loads settings from:
1. Environment variables (highest priority)
2. .env file (if exists)
3. Default values defined below (lowest priority)

To configure, create/edit .env file in the app directory.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings for B2Bmarket portal backend.
    
    Settings are automatically loaded from .env file.
    Values in .env will override the defaults below.
    """

    APP_NAME: str = "B2Bmarket"
    APP_URL: str = "http://localhost:3000"
    DATABASE_URL: str = "postgresql://localhost/b2bmarket"
    DATABASE_UT_URL: str = "sqlite:///./test_b2bmarket.db"
    FRONTEND_URL: str = "http://localhost:3000"
    UVICORN_PORT: str = "8210"
    DEBUG: bool = False
    JWT_SECRET: str = "your-secret-key-change-in-production-use-openssl-rand-hex-32"

    # Automatically load from .env file
    model_config = {"env_file": ".env", "extra": "allow"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
