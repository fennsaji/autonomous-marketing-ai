"""
Tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


def test_register_user(client: TestClient, test_user_data: dict):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]
    assert "id" in data


def test_register_duplicate_email(client: TestClient, test_user_data: dict):
    """Test registration with duplicate email."""
    # Register first user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Try to register with same email
    response = client.post("/api/v1/auth/register", json=test_user_data)
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_valid_credentials(client: TestClient, test_user_data: dict):
    """Test login with valid credentials."""
    # Register user first
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Login
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data


def test_login_invalid_credentials(client: TestClient, test_user_data: dict):
    """Test login with invalid credentials."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_get_current_user(client: TestClient, test_user_data: dict):
    """Test getting current user information."""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login", 
        data={"username": test_user_data["email"], "password": test_user_data["password"]}
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]


def test_logout(client: TestClient, test_user_data: dict):
    """Test user logout."""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login", 
        data={"username": test_user_data["email"], "password": test_user_data["password"]}
    )
    token = login_response.json()["access_token"]
    
    # Logout
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/v1/auth/logout", headers=headers)
    
    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]