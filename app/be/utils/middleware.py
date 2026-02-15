"""Middleware utilities for B2Bmarket backend."""
import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses."""

    async def dispatch(self, request: Request, call_next):
        """Log incoming requests and outgoing responses."""
        start_time = time.time()

        # Log incoming request
        log.info(f"→ {request.method} {request.url.path}")
        if request.query_params:
            log.debug(f"  Query params: {dict(request.query_params)}")

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log response
            log.info(
                f"← {request.method} {request.url.path} "
                f"Status: {response.status_code} "
                f"Time: {process_time:.3f}s"
            )

            return response
        except Exception as e:
            process_time = time.time() - start_time
            log.error(
                f"✗ {request.method} {request.url.path} "
                f"Error after {process_time:.3f}s: {type(e).__name__}: {str(e)}",
                exc_info=True
            )
            raise
