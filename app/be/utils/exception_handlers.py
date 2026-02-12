"""Exception handlers for B2Bmarket backend."""
import logging
import traceback

from config import get_settings
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException

settings = get_settings()
log = logging.getLogger(__name__)


def setup_exception_handlers(app):
    """Register exception handlers for the FastAPI app."""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions (like 401, 404, etc.)."""
        log.warning(
            f"HTTP {exc.status_code} on {request.method} {request.url.path}: {exc.detail}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors."""
        log.warning(
            f"Validation error on {request.method} {request.url.path}: {exc.errors()}"
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler to log all unhandled errors."""
        log.error(
            f"❌ UNHANDLED EXCEPTION on {request.method} {request.url.path}\n"
            f"   Type: {type(exc).__name__}\n"
            f"   Message: {str(exc)}\n"
            f"   Traceback:\n{traceback.format_exc()}",
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "error": str(exc) if settings.DEBUG else "An error occurred",
            },
        )
