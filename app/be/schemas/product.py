"""Pydantic schemas for Product API."""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """Request body for creating a product. vendor_id is set from the logged-in vendor."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    sku: Optional[str] = Field(None, max_length=100, description="Stock keeping unit")
    description: Optional[str] = Field(None, description="Product description")
    price: Decimal = Field(..., ge=0, description="Unit price")


class ProductUpdate(BaseModel):
    """Request body for updating a product (partial)."""

    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Product name")
    sku: Optional[str] = Field(None, max_length=100, description="Stock keeping unit")
    description: Optional[str] = Field(None, description="Product description")
    price: Optional[Decimal] = Field(None, ge=0, description="Unit price")
    vendor_id: Optional[int] = Field(None, gt=0, description="Vendor ID")


class ProductResponse(BaseModel):
    """Response body for a single product."""

    model_config = ConfigDict(extra="forbid")

    id: int = Field(..., description="Product ID")
    name: str = Field(..., description="Product name")
    sku: Optional[str] = Field(None, description="Stock keeping unit")
    description: Optional[str] = Field(None, description="Product description")
    price: Decimal = Field(..., description="Unit price")
    vendor_id: int = Field(..., description="Vendor ID")
    vendor_name: Optional[str] = Field(None, description="Vendor company name")
    created_at: datetime = Field(..., description="Creation timestamp")
