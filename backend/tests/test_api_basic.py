"""
Basic API tests without database dependency.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create a test client without database dependency
client = TestClient(app)


@pytest.mark.unit
def test_root_endpoint():
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
def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data


@pytest.mark.unit
def test_api_v1_root():
    """Test API v1 root endpoint."""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Defeah Marketing API v1"


@pytest.mark.unit
def test_api_v1_health():
    """Test API v1 health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "v1"


@pytest.mark.unit
def test_docs_endpoint():
    """Test docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.unit
def test_openapi_json():
    """Test OpenAPI JSON endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "Defeah Marketing Backend"