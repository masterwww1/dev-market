"""Pydantic schemas for health API."""
from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """Response body for GET /api/health/."""

    model_config = ConfigDict(extra="forbid")

    app: str = Field(..., description="Application name")
    status: str = Field(..., description="Overall status: healthy | degraded")
    database: str = Field(..., description="Database status: ok | error")
