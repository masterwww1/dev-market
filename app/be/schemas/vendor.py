"""Pydantic schemas for Vendor API."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class VendorCreate(BaseModel):
    """Request body for creating a vendor."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255, description="Vendor name")


class VendorResponse(BaseModel):
    """Response body for a single vendor."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(..., description="Vendor ID")
    name: str = Field(..., description="Vendor name")
    created_at: datetime = Field(..., description="Creation timestamp")
