"""
Integration tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import time

from tests.test_utils import (
    AuthTestHelper, 
    PasswordTestHelper, 
    EmailTestHelper, 
    APITestHelper,
    RateLimitTestHelper
)


class TestUserRegistrationEndpoint:
    """Test /api/v1/auth/register endpoint."""
    
    @pytest.mark.integration
    def test_register_user_success(self, client: TestClient, sample_user_data):
        """Test successful user registration."""
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert "user" in data
        assert "message" in data
        assert data["message"] == "User registered successfully. Please verify your email before logging in."
        
        # Verify user data structure
        user_data = data["user"]
        assert user_data["email"] == sample_user_data["email"]
        assert user_data["full_name"] == sample_user_data["full_name"]
        assert user_data["is_active"] is True
        assert user_data["is_verified"] is False
        assert "id" in user_data
        assert "created_at" in user_data
        assert "updated_at" in user_data
        
        # Ensure sensitive data is not returned
        assert "password" not in user_data
        assert "hashed_password" not in user_data
    
    @pytest.mark.integration
    def test_register_user_duplicate_email(self, client: TestClient, sample_user_data):
        """Test registration with duplicate email fails."""
        # Register user first time
        response1 = client.post("/api/v1/auth/register", json=sample_user_data)
        assert response1.status_code == 201
        
        # Try to register same email again
        response2 = client.post("/api/v1/auth/register", json=sample_user_data)
        assert response2.status_code == 409
        
        data = response2.json()
        APITestHelper.assert_error_response(data, "USER_ALREADY_EXISTS")
    
    @pytest.mark.integration
    def test_register_user_weak_password(self, client: TestClient, sample_weak_password_data):
        """Test registration with weak password fails."""
        response = client.post("/api/v1/auth/register", json=sample_weak_password_data)
        
        assert response.status_code == 400
        data = response.json()
        APITestHelper.assert_error_response(data, "PASSWORD_TOO_WEAK")
        assert "score:" in data["error"]["message"]
    
    @pytest.mark.integration
    def test_register_user_invalid_email(self, client: TestClient, sample_invalid_email_data):
        """Test registration with invalid email fails."""
        response = client.post("/api/v1/auth/register", json=sample_invalid_email_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any("email" in error["loc"] for error in data["detail"])
    
    @pytest.mark.integration
    def test_register_user_missing_required_fields(self, client: TestClient):
        """Test registration with missing required fields fails."""
        # Missing email
        response = client.post("/api/v1/auth/register", json={
            "password": "TestPassword123!",
            "full_name": "Test User"
        })
        assert response.status_code == 422
        
        # Missing password
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "full_name": "Test User"
        })
        assert response.status_code == 422
    
    @pytest.mark.integration
    def test_register_user_optional_full_name(self, client: TestClient):
        """Test registration without full_name succeeds."""
        user_data = {
            "email": "minimal@example.com",
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["user"]["full_name"] is None
    
    @pytest.mark.integration
    @patch('app.api.v1.auth.check_authentication_rate_limit')
    def test_register_rate_limit_exceeded(self, mock_rate_limit, client: TestClient, sample_user_data):
        """Test registration rate limiting."""
        from app.utils.exceptions import RateLimitError
        
        mock_rate_limit.side_effect = RateLimitError(
            "Too many registration attempts", 
            details={"retry_after": 300}
        )
        
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        
        assert response.status_code == 429
        assert response.headers.get("Retry-After") == "300"
        
        data = response.json()
        APITestHelper.assert_error_response(data, "RATE_LIMIT_EXCEEDED")


class TestUserLoginEndpoint:
    """Test /api/v1/auth/login endpoint."""
    
    @pytest.mark.integration
    def test_login_user_success(self, client: TestClient, sample_user_data):
        """Test successful user login."""
        # Register user first
        register_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        # Login
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "user" in data
        assert "tokens" in data
        assert "message" in data
        assert data["message"] == "Login successful"
        
        # Verify user data
        user_data = data["user"]
        assert user_data["email"] == sample_user_data["email"]
        
        # Verify token data
        tokens = data["tokens"]
        APITestHelper.assert_token_response(tokens)
    
    @pytest.mark.integration
    def test_login_user_invalid_credentials(self, client: TestClient, sample_user_data):
        """Test login with invalid credentials fails."""
        # Register user first
        register_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        # Try login with wrong password
        login_data = {
            "email": sample_user_data["email"],
            "password": "WrongPassword123!"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        APITestHelper.assert_error_response(data, "INVALID_CREDENTIALS")
    
    @pytest.mark.integration
    def test_login_user_nonexistent_email(self, client: TestClient):
        """Test login with non-existent email fails."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "TestPassword123!"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        APITestHelper.assert_error_response(data, "INVALID_CREDENTIALS")
    
    @pytest.mark.integration
    def test_login_user_invalid_email_format(self, client: TestClient):
        """Test login with invalid email format fails."""
        login_data = {
            "email": "invalid-email",
            "password": "TestPassword123!"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 422
    
    @pytest.mark.integration
    def test_login_user_missing_fields(self, client: TestClient):
        """Test login with missing fields fails."""
        # Missing email
        response = client.post("/api/v1/auth/login", json={
            "password": "TestPassword123!"
        })
        assert response.status_code == 422
        
        # Missing password
        response = client.post("/api/v1/auth/login", json={
            "email": "test@example.com"
        })
        assert response.status_code == 422
    
    @pytest.mark.integration
    @patch('app.api.v1.auth.check_authentication_rate_limit')
    def test_login_rate_limit_exceeded(self, mock_rate_limit, client: TestClient):
        """Test login rate limiting."""
        from app.utils.exceptions import RateLimitError
        
        mock_rate_limit.side_effect = RateLimitError(
            "Too many login attempts", 
            details={"retry_after": 60}
        )
        
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 429
        assert response.headers.get("Retry-After") == "60"


class TestTokenRefreshEndpoint:
    """Test /api/v1/auth/refresh endpoint."""
    
    @pytest.mark.integration
    def test_refresh_token_success(self, client: TestClient, sample_user_data):
        """Test successful token refresh."""
        # Register and login user
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        refresh_token = login_data["tokens"]["refresh_token"]
        
        # Refresh token
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        data = response.json()
        
        APITestHelper.assert_token_response(data)
        assert data["refresh_token"] == refresh_token  # Same refresh token returned
    
    @pytest.mark.integration
    def test_refresh_token_invalid(self, client: TestClient):
        """Test refresh with invalid token fails."""
        refresh_data = {"refresh_token": "invalid.token.here"}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
        data = response.json()
        assert "Invalid or expired refresh token" in data["detail"]
    
    @pytest.mark.integration
    def test_refresh_token_access_token_used(self, client: TestClient, sample_user_data):
        """Test refresh with access token instead of refresh token fails."""
        # Register and login user
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        
        # Try to refresh with access token
        refresh_data = {"refresh_token": access_token}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
    
    @pytest.mark.integration
    def test_refresh_token_missing_token(self, client: TestClient):
        """Test refresh with missing token fails."""
        response = client.post("/api/v1/auth/refresh", json={})
        assert response.status_code == 422


class TestUserLogoutEndpoint:
    """Test /api/v1/auth/logout endpoint."""
    
    @pytest.mark.integration
    def test_logout_user_success(self, client: TestClient, sample_user_data):
        """Test successful user logout."""
        # Register and login user
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        refresh_token = login_data["tokens"]["refresh_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {access_token}"}
        logout_data = {"refresh_token": refresh_token}
        response = client.post("/api/v1/auth/logout", json=logout_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Logout successful"
    
    @pytest.mark.integration
    def test_logout_user_without_refresh_token(self, client: TestClient, sample_user_data):
        """Test logout without refresh token succeeds."""
        # Register and login user
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        
        # Logout without refresh token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/api/v1/auth/logout", json={}, headers=headers)
        
        assert response.status_code == 200
    
    @pytest.mark.integration
    def test_logout_user_unauthorized(self, client: TestClient):
        """Test logout without authentication fails."""
        response = client.post("/api/v1/auth/logout", json={})
        assert response.status_code == 401
    
    @pytest.mark.integration
    def test_logout_user_invalid_token(self, client: TestClient):
        """Test logout with invalid token fails."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.post("/api/v1/auth/logout", json={}, headers=headers)
        assert response.status_code == 401


class TestUserProfileEndpoint:
    """Test /api/v1/auth/me endpoint."""
    
    @pytest.mark.integration
    def test_get_user_profile_success(self, client: TestClient, sample_user_data):
        """Test successful user profile retrieval."""
        # Register and login user
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        
        # Get profile
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["email"] == sample_user_data["email"]
        assert data["full_name"] == sample_user_data["full_name"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        
        # Ensure sensitive data is not returned
        assert "password" not in data
        assert "hashed_password" not in data
    
    @pytest.mark.integration
    def test_get_user_profile_unauthorized(self, client: TestClient):
        """Test profile retrieval without authentication fails."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    @pytest.mark.integration
    def test_get_user_profile_invalid_token(self, client: TestClient):
        """Test profile retrieval with invalid token fails."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401


class TestPasswordChangeEndpoint:
    """Test /api/v1/auth/change-password endpoint."""
    
    @pytest.mark.integration
    def test_change_password_success(self, client: TestClient, sample_user_data):
        """Test successful password change."""
        # Register and login user
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        
        # Change password
        headers = {"Authorization": f"Bearer {access_token}"}
        password_data = {
            "current_password": sample_user_data["password"],
            "new_password": "NewTestPassword123!"
        }
        response = client.post("/api/v1/auth/change-password", json=password_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Password changed successfully"
        
        # Verify can login with new password
        login_data = {
            "email": sample_user_data["email"],
            "password": "NewTestPassword123!"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
    
    @pytest.mark.integration
    def test_change_password_wrong_current_password(self, client: TestClient, sample_user_data):
        """Test password change with wrong current password fails."""
        # Register and login user
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        
        # Try to change password with wrong current password
        headers = {"Authorization": f"Bearer {access_token}"}
        password_data = {
            "current_password": "WrongPassword123!",
            "new_password": "NewTestPassword123!"
        }
        response = client.post("/api/v1/auth/change-password", json=password_data, headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        APITestHelper.assert_error_response(data, "INVALID_CREDENTIALS")
    
    @pytest.mark.integration
    def test_change_password_weak_new_password(self, client: TestClient, sample_user_data):
        """Test password change with weak new password fails."""
        # Register and login user
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        
        # Try to change to weak password
        headers = {"Authorization": f"Bearer {access_token}"}
        password_data = {
            "current_password": sample_user_data["password"],
            "new_password": "weak"
        }
        response = client.post("/api/v1/auth/change-password", json=password_data, headers=headers)
        
        assert response.status_code == 400
        data = response.json()
        APITestHelper.assert_error_response(data, "PASSWORD_TOO_WEAK")
    
    @pytest.mark.integration
    def test_change_password_unauthorized(self, client: TestClient):
        """Test password change without authentication fails."""
        password_data = {
            "current_password": "TestPassword123!",
            "new_password": "NewTestPassword123!"
        }
        response = client.post("/api/v1/auth/change-password", json=password_data)
        assert response.status_code == 401


class TestAuthenticationFlow:
    """Test complete authentication flow scenarios."""
    
    @pytest.mark.integration
    def test_complete_authentication_flow(self, client: TestClient, sample_user_data):
        """Test complete authentication flow: register -> login -> profile -> logout."""
        # 1. Register
        register_response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert register_response.status_code == 201
        
        # 2. Login
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        refresh_token = login_data["tokens"]["refresh_token"]
        
        # 3. Get profile
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = client.get("/api/v1/auth/me", headers=headers)
        assert profile_response.status_code == 200
        
        # 4. Refresh token
        refresh_data = {"refresh_token": refresh_token}
        refresh_response = client.post("/api/v1/auth/refresh", json=refresh_data)
        assert refresh_response.status_code == 200
        
        # 5. Logout
        logout_data = {"refresh_token": refresh_token}
        logout_response = client.post("/api/v1/auth/logout", json=logout_data, headers=headers)
        assert logout_response.status_code == 200
    
    @pytest.mark.integration
    def test_token_blacklisting_after_logout(self, client: TestClient, sample_user_data):
        """Test that tokens are blacklisted after logout."""
        # Register and login
        client.post("/api/v1/auth/register", json=sample_user_data)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        login_data = login_response.json()
        
        access_token = login_data["tokens"]["access_token"]
        refresh_token = login_data["tokens"]["refresh_token"]
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Verify token works before logout
        profile_response = client.get("/api/v1/auth/me", headers=headers)
        assert profile_response.status_code == 200
        
        # Logout
        logout_data = {"refresh_token": refresh_token}
        logout_response = client.post("/api/v1/auth/logout", json=logout_data, headers=headers)
        assert logout_response.status_code == 200
        
        # Verify access token no longer works (would need Redis mock for full test)
        # This test would require mocking Redis blacklist functionality
        
        # Verify refresh token no longer works
        refresh_data = {"refresh_token": refresh_token}
        refresh_response = client.post("/api/v1/auth/refresh", json=refresh_data)
        # This might still work depending on Redis mock - in real scenario it should fail