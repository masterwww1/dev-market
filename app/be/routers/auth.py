"""Authentication API for B2Bmarket."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from be.database import get_db
from be.models.user import User
from be.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    VerifyTokenRequest,
    VerifyTokenResponse,
)
from be.utils.jwt import create_access_token, create_refresh_token, verify_token, decode_token_without_verification
from be.utils.password import verify_password, generate_salt

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(body: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    """
    Login with email and password.
    Returns JWT access token and refresh token.
    """
    # Get user from database
    user = (
        db.query(User)
        .filter(func.lower(User.email) == body.email.lower())
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Check if user is active
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    # Check user status
    if user.status and user.status not in ("ACTIVE", "VERIFIED"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account not verified",
        )

    # Verify password
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Generate new salt and update user
    salt = generate_salt()
    user.salt = salt
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create tokens
    token_payload = {
        "sub": user.email,
        "user_id": user.id,
        "source": "EMAIL",
    }

    access_token = create_access_token(token_payload, salt)
    refresh_token = create_refresh_token(token_payload, salt)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=900,  # 15 minutes in seconds
        user={"id": user.id, "email": user.email},
    )


@router.post("/refresh", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK)
def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)) -> RefreshTokenResponse:
    """
    Refresh access token using refresh token.
    """
    refresh_token_str = body.refresh_token

    if not refresh_token_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token is required",
        )

    # Decode token without verification first to get user_id
    try:
        decoded = decode_token_without_verification(refresh_token_str)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Check token type
    if decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    # Get user from database
    user_id = decoded.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    # Verify token with user's salt
    try:
        verify_token(refresh_token_str, user.salt or "")
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # Create new access token
    token_payload = {
        "sub": user.email,
        "user_id": user.id,
        "source": decoded.get("source", "EMAIL"),
    }

    new_access_token = create_access_token(token_payload, user.salt or "")

    return RefreshTokenResponse(
        access_token=new_access_token,
        token_type="Bearer",
        expires_in=900,
    )


@router.post("/verify", response_model=VerifyTokenResponse, status_code=status.HTTP_200_OK)
def verify_token_endpoint(body: VerifyTokenRequest, db: Session = Depends(get_db)) -> VerifyTokenResponse:
    """
    Verify access token and return user information.
    """
    token = body.token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token is required",
        )

    # Decode token without verification first to get user_id
    try:
        decoded = decode_token_without_verification(token)
    except HTTPException:
        return VerifyTokenResponse(
            valid=False,
            user={},
            payload={},
        )

    # Check token type
    if decoded.get("type") != "access":
        return VerifyTokenResponse(
            valid=False,
            user={},
            payload={},
        )

    # Get user from database
    user_id = decoded.get("user_id")
    if not user_id:
        return VerifyTokenResponse(
            valid=False,
            user={},
            payload={},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return VerifyTokenResponse(
            valid=False,
            user={},
            payload={},
        )

    if not user.active:
        return VerifyTokenResponse(
            valid=False,
            user={},
            payload={},
        )

    # Verify token with user's salt
    try:
        verify_token(token, user.salt or "")
    except HTTPException:
        return VerifyTokenResponse(
            valid=False,
            user={},
            payload={},
        )

    return VerifyTokenResponse(
        valid=True,
        user={"id": user.id, "email": user.email},
        payload={
            "sub": decoded.get("sub"),
            "user_id": decoded.get("user_id"),
            "source": decoded.get("source", "EMAIL"),
        },
    )
