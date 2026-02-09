"""Pydantic schemas for ping API."""
from pydantic import BaseModel, ConfigDict, Field


class PingResponse(BaseModel):
    """Response body for GET /api/ping/."""

    model_config = ConfigDict(extra="forbid")

    status: str = Field(..., description="Status string, e.g. 'ok'")
