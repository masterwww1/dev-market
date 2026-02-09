"""B2Bmarket B2B marketplace portal - FastAPI backend."""
import logging

from config import get_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from be.routers import health, ping, vendors

settings = get_settings()
log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s %(name)s - %(message)s",
)

app = FastAPI(
    title="B2Bmarket API",
    description="B2B marketplace portal backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(vendors.router, prefix="/api")


@app.get("/")
async def root():
    """Root redirect/info."""
    return {"app": "B2Bmarket", "docs": "/docs"}


@app.get("/api/info")
async def info():
    """API info for B2Bmarket portal."""
    return {
        "APP_NAME": settings.APP_NAME,
        "APP_URL": settings.APP_URL,
        "UVICORN_PORT": settings.UVICORN_PORT,
    }
