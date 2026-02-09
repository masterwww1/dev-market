"""TDD tests for B2Bmarket health API."""
import pytest
from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    """Health endpoint returns 200."""
    response = client.get("/api/health/")
    assert response.status_code == 200


def test_health_returns_b2bmarket_app(client: TestClient) -> None:
    """Health response includes B2Bmarket app name."""
    response = client.get("/api/health/")
    data = response.json()
    assert data["app"] == "B2Bmarket"
    assert data["status"] in ("healthy", "degraded")
    assert "database" in data
