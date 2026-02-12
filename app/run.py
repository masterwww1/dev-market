"""Startup script for B2Bmarket backend server.

This script reads the port configuration from .env file (UVICORN_PORT)
and starts the FastAPI application using uvicorn.

Usage:
    python run.py

The port can be configured in .env file:
    UVICORN_PORT=8210
"""
import uvicorn

from config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    port = int(settings.UVICORN_PORT)
    
    print(f"Starting B2Bmarket backend on http://127.0.0.1:{port}")
    print(f"API docs available at http://127.0.0.1:{port}/docs")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=port,
        reload=True,
        log_level="info",
    )
