"""B2Bmarket B2B marketplace portal - FastAPI backend."""
from config import get_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from be.routers import auth, health, ping, vendors, products
from be.utils.logging_config import setup_logging
from be.utils.middleware import LoggingMiddleware
from be.utils.exception_handlers import setup_exception_handlers

settings = get_settings()

# Setup logging configuration
setup_logging()

app = FastAPI(
    title="B2Bmarket API",
    description="B2B marketplace portal backend",
    version="0.1.0",
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(ping.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(vendors.router, prefix="/api")
app.include_router(products.router, prefix="/api")

# Setup exception handlers
setup_exception_handlers(app)


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
