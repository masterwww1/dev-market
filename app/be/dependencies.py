"""FastAPI dependencies for B2Bmarket."""
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from be.database import get_db
from be.models.user import User
from be.utils.jwt import decode_token_without_verification, verify_token


class CurrentUser:
    """Authenticated user from JWT. Vendor is resolved by matching user email to vendor email."""

    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> CurrentUser:
    """Extract and validate JWT from Authorization header; return current user."""
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )
    token = auth[7:].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )
    try:
        decoded = decode_token_without_verification(token)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    if decoded.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    user_id = decoded.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    try:
        verify_token(token, user.salt or "")
    except HTTPException:
        raise
    return CurrentUser(id=user.id, email=user.email)
