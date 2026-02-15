"""Pydantic schemas for Vendor API."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VendorCreate(BaseModel):
    """Request body for creating a vendor."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255, description="Vendor name")
    first_name: Optional[str] = Field(None, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, max_length=100, description="Last name")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    phone_number: Optional[str] = Field(None, max_length=20, description="Phone number")


class VendorUpdate(BaseModel):
    """Request body for updating a vendor (partial)."""

    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Vendor name")
    first_name: Optional[str] = Field(None, max_length=100, description="First name")
    last_name: Optional[str] = Field(None, max_length=100, description="Last name")
    email: Optional[str] = Field(None, max_length=255, description="Email address")
    phone_number: Optional[str] = Field(None, max_length=20, description="Phone number")


class VendorResponse(BaseModel):
    """Response body for a single vendor."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(..., description="Vendor ID")
    name: str = Field(..., description="Vendor name")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    email: Optional[str] = Field(None, description="Email address")
    phone_number: Optional[str] = Field(None, description="Phone number")
    created_at: datetime = Field(..., description="Creation timestamp")
