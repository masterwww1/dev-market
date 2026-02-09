"""Health ping endpoint for B2Bmarket API."""
from fastapi import APIRouter, status

from be.schemas.ping import PingResponse

router = APIRouter(prefix="/ping", tags=["Ping"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=PingResponse)
async def get_ping() -> PingResponse:
    """Return 200 OK for liveness/readiness checks."""
    return PingResponse(status="ok")
