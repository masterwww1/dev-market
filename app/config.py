"""B2Bmarket backend configuration."""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings for B2Bmarket portal backend."""

    APP_NAME: str = "B2Bmarket"
    APP_URL: str = "http://localhost:3000"
    DATABASE_URL: str = "postgresql://localhost/b2bmarket"
    DATABASE_UT_URL: str = "sqlite:///./test_b2bmarket.db"
    FRONTEND_URL: str = "http://localhost:3000"
    UVICORN_PORT: str = "8000"
    DEBUG: bool = False

    model_config = {"env_file": ".env", "extra": "allow"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
