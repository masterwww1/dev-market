"""TDD tests for B2Bmarket Authentication API."""
import pytest
from fastapi.testclient import TestClient
from be.utils.password import hash_password
from be.models.user import User


def test_login_success(client: TestClient, db_session) -> None:
    """POST /api/auth/login returns tokens for valid credentials."""
    # Create a test user
    user = User(
        email="test@example.com",
        password_hash=hash_password("password123"),
        active=True,
        status="ACTIVE",
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user"]["email"] == "test@example.com"


def test_login_invalid_credentials(client: TestClient, db_session) -> None:
    """POST /api/auth/login returns 401 for invalid credentials."""
    # Create a test user
    user = User(
        email="test@example.com",
        password_hash=hash_password("password123"),
        active=True,
        status="ACTIVE",
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_user_not_found(client: TestClient) -> None:
    """POST /api/auth/login returns 401 for non-existent user."""
    response = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401


def test_refresh_token(client: TestClient, db_session) -> None:
    """POST /api/auth/refresh returns new access token."""
    # Create user and login
    user = User(
        email="test@example.com",
        password_hash=hash_password("password123"),
        active=True,
        status="ACTIVE",
    )
    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]

    # Refresh token
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"


def test_verify_token(client: TestClient, db_session) -> None:
    """POST /api/auth/verify returns user info for valid token."""
    # Create user and login
    user = User(
        email="test@example.com",
        password_hash=hash_password("password123"),
        active=True,
        status="ACTIVE",
    )
    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # Verify token
    response = client.post(
        "/api/auth/verify",
        json={"token": access_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["user"]["email"] == "test@example.com"
