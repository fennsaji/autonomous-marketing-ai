"""
Test main application endpoints.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_root_endpoint(client: TestClient):
    """Test root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "environment" in data
    assert data["message"] == "Defeah Marketing Backend"
    assert data["version"] == "1.0.0"


@pytest.mark.unit
def test_health_endpoint(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert "database" in data["services"]
    assert "redis" in data["services"]


@pytest.mark.unit
def test_api_v1_root(client: TestClient):
    """Test API v1 root endpoint."""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Defeah Marketing API v1"


@pytest.mark.unit
def test_api_v1_health(client: TestClient):
    """Test API v1 health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "v1"