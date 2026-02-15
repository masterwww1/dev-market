"""JWT token utilities for B2Bmarket authentication."""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from config import get_settings

settings = get_settings()

# JWT Configuration
JWT_SECRET = getattr(settings, "JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 days


def create_access_token(data: dict, salt: str) -> str:
    """
    Create an access token with the data and expiration time.

    Args:
        data: Data to be encoded in the token (e.g., {"sub": email, "user_id": id})
        salt: User salt for additional security

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access", "salt": salt})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET + salt, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, salt: str) -> str:
    """
    Create a refresh token with the data and expiration time.

    Args:
        data: Data to be encoded in the token
        salt: User salt for additional security

    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh", "salt": salt})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET + salt, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, salt: str) -> dict:
    """
    Verify and decode JWT token.

    Args:
        token: JWT token to verify
        salt: User salt for verification

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )

    try:
        payload = jwt.decode(token, JWT_SECRET + salt, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def decode_token_without_verification(token: str) -> dict:
    """
    Decode token without verification (for inspection only).

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token cannot be decoded
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )

    try:
        decoded_token = jwt.decode(
            token,
            key=None,
            options={"verify_signature": False, "verify_exp": False},
        )
        return decoded_token
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
