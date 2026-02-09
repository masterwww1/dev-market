"""TDD tests for B2Bmarket Vendors API."""
import pytest
from fastapi.testclient import TestClient


def test_list_vendors_empty(client: TestClient) -> None:
    """GET /api/vendors/ returns empty list when no vendors."""
    response = client.get("/api/vendors/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_vendor(client: TestClient) -> None:
    """POST /api/vendors/ creates a vendor and returns 201."""
    response = client.post("/api/vendors/", json={"name": "Acme Corp"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Acme Corp"
    assert "id" in data
    assert "created_at" in data


def test_list_vendors_after_create(client: TestClient) -> None:
    """GET /api/vendors/ returns created vendors."""
    client.post("/api/vendors/", json={"name": "Vendor One"})
    client.post("/api/vendors/", json={"name": "Vendor Two"})
    response = client.get("/api/vendors/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    names = {i["name"] for i in items}
    assert names == {"Vendor One", "Vendor Two"}
