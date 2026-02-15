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


def test_get_vendor(client: TestClient) -> None:
    """GET /api/vendors/{id} returns the vendor."""
    create = client.post("/api/vendors/", json={"name": "Acme"})
    assert create.status_code == 201
    vid = create.json()["id"]
    response = client.get(f"/api/vendors/{vid}")
    assert response.status_code == 200
    assert response.json()["name"] == "Acme"


def test_get_vendor_404(client: TestClient) -> None:
    """GET /api/vendors/{id} returns 404 when not found."""
    response = client.get("/api/vendors/99999")
    assert response.status_code == 404


def test_update_vendor(client: TestClient) -> None:
    """PATCH /api/vendors/{id} updates the vendor."""
    create = client.post("/api/vendors/", json={"name": "Old Name"})
    assert create.status_code == 201
    vid = create.json()["id"]
    response = client.patch(f"/api/vendors/{vid}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_update_vendor_404(client: TestClient) -> None:
    """PATCH /api/vendors/{id} returns 404 when not found."""
    response = client.patch("/api/vendors/99999", json={"name": "X"})
    assert response.status_code == 404


def test_delete_vendor(client: TestClient) -> None:
    """DELETE /api/vendors/{id} removes the vendor and returns 204."""
    create = client.post("/api/vendors/", json={"name": "To Delete"})
    assert create.status_code == 201
    vid = create.json()["id"]
    response = client.delete(f"/api/vendors/{vid}")
    assert response.status_code == 204
    get_resp = client.get(f"/api/vendors/{vid}")
    assert get_resp.status_code == 404


def test_delete_vendor_404(client: TestClient) -> None:
    """DELETE /api/vendors/{id} returns 404 when not found."""
    response = client.delete("/api/vendors/99999")
    assert response.status_code == 404
