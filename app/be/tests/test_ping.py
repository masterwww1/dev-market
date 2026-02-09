"""TDD tests for B2Bmarket ping API."""
import pytest
from fastapi.testclient import TestClient


def test_ping_returns_200(client: TestClient) -> None:
    """Ping endpoint returns 200 OK."""
    response = client.get("/api/ping/")
    assert response.status_code == 200


def test_ping_returns_ok_status(client: TestClient) -> None:
    """Ping response body contains status ok."""
    response = client.get("/api/ping/")
    assert response.json() == {"status": "ok"}
