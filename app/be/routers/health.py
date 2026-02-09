"""Health check endpoint for B2Bmarket API."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from be.database import get_db
from be.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def get_health(db: Session = Depends(get_db)) -> HealthResponse:
    """Return app and database health status."""
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False
    return HealthResponse(
        app="B2Bmarket",
        status="healthy" if db_ok else "degraded",
        database="ok" if db_ok else "error",
    )
