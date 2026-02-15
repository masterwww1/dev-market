"""Pydantic schemas for authentication API."""
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    """Request body for login."""

    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=1, description="User password")


class RefreshTokenRequest(BaseModel):
    """Request body for token refresh."""

    model_config = ConfigDict(extra="forbid")

    refresh_token: str = Field(..., description="Refresh token")


class VerifyTokenRequest(BaseModel):
    """Request body for token verification."""

    model_config = ConfigDict(extra="forbid")

    token: str = Field(..., description="Access token to verify")


class LoginResponse(BaseModel):
    """Response body for login."""

    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(default=900, description="Access token expiry in seconds")
    user: dict = Field(..., description="User information")


class RefreshTokenResponse(BaseModel):
    """Response body for token refresh."""

    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(..., description="New JWT access token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(default=900, description="Access token expiry in seconds")


class VerifyTokenResponse(BaseModel):
    """Response body for token verification."""

    model_config = ConfigDict(extra="forbid")

    valid: bool = Field(..., description="Whether token is valid")
    user: dict = Field(..., description="User information")
    payload: dict = Field(..., description="Token payload")
