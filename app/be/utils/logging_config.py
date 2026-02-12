"""Logging configuration for B2Bmarket backend."""
import logging

from config import get_settings

settings = get_settings()


def setup_logging():
    """Configure logging for the application."""
    # Configure logging with more detail
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="%(levelname)s %(asctime)s [%(name)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set specific loggers to appropriate levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)  # Reduce access log noise
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)  # Reduce SQL log noise unless DEBUG
