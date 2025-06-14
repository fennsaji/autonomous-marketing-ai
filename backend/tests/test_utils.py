"""
Authentication test utilities and helpers.
"""
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.auth import create_access_token, create_refresh_token, hash_password
from app.models.user import User
from app.services.user_service import UserService


class AuthTestHelper:
    """Helper class for authentication testing."""
    
    @staticmethod
    def create_test_user_data(
        email: str = "test@example.com",
        password: str = "TestPassword123!",
        full_name: str = "Test User",
        **kwargs
    ) -> Dict[str, Any]:
        """Create test user data with default values."""
        return {
            "email": email,
            "password": password,
            "full_name": full_name,
            **kwargs
        }
    
    @staticmethod
    def create_test_user_in_db(
        session: Session,
        email: str = "test@example.com",
        password: str = "TestPassword123!",
        full_name: str = "Test User",
        is_active: bool = True,
        is_verified: bool = True,
        **kwargs
    ) -> User:
        """Create a test user directly in the database."""
        user = User(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            is_active=is_active,
            is_verified=is_verified,
            **kwargs
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    @staticmethod
    async def create_test_user_in_db_async(
        session: AsyncSession,
        email: str = "test@example.com",
        password: str = "TestPassword123!",
        full_name: str = "Test User",
        is_active: bool = True,
        is_verified: bool = True,
        **kwargs
    ) -> User:
        """Create a test user directly in the async database."""
        user = User(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            is_active=is_active,
            is_verified=is_verified,
            **kwargs
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    @staticmethod
    def create_test_tokens(user_id: str) -> Dict[str, str]:
        """Create test access and refresh tokens for a user."""
        access_token = create_access_token(data={"sub": user_id})
        refresh_token = create_refresh_token(data={"sub": user_id})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def create_expired_token(user_id: str) -> str:
        """Create an expired access token for testing."""
        # Create token that expired 1 hour ago
        expired_time = datetime.utcnow() - timedelta(hours=1)
        return create_access_token(
            data={"sub": user_id}, 
            expires_delta=timedelta(seconds=-3600)  # Negative delta for expired token
        )
    
    @staticmethod
    def get_auth_headers(token: str) -> Dict[str, str]:
        """Get authorization headers with bearer token."""
        return {"Authorization": f"Bearer {token}"}
    
    @staticmethod
    def register_test_user(
        client: TestClient,
        user_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Register a test user via API and return response."""
        if user_data is None:
            user_data = AuthTestHelper.create_test_user_data()
        
        response = client.post("/api/v1/auth/register", json=user_data)
        return response.json() if response.status_code == 201 else None
    
    @staticmethod
    def login_test_user(
        client: TestClient,
        email: str = "test@example.com",
        password: str = "TestPassword123!"
    ) -> Dict[str, Any]:
        """Login a test user via API and return response with tokens."""
        login_data = {"email": email, "password": password}
        response = client.post("/api/v1/auth/login", json=login_data)
        return response.json() if response.status_code == 200 else None
    
    @staticmethod
    def create_authenticated_client(
        client: TestClient,
        user: Optional[User] = None
    ) -> tuple[TestClient, str]:
        """
        Create an authenticated test client with a logged-in user.
        Returns tuple of (client, access_token).
        """
        if user is None:
            # Register and login a test user
            user_data = AuthTestHelper.create_test_user_data()
            AuthTestHelper.register_test_user(client, user_data)
            login_response = AuthTestHelper.login_test_user(
                client, user_data["email"], user_data["password"]
            )
            access_token = login_response["tokens"]["access_token"]
        else:
            # Create token for existing user
            tokens = AuthTestHelper.create_test_tokens(str(user.id))
            access_token = tokens["access_token"]
        
        # Set default authorization header
        client.headers.update(AuthTestHelper.get_auth_headers(access_token))
        
        return client, access_token


class PasswordTestHelper:
    """Helper class for password testing scenarios."""
    
    WEAK_PASSWORDS = [
        "weak",
        "12345678",
        "password",
        "abcdefgh",
        "ABCDEFGH",
        "12345abc",
    ]
    
    STRONG_PASSWORDS = [
        "TestPassword123!",
        "MySecure@Pass2024",
        "Complex#Password99",
        "Strong&Password123",
        "Secure*Key2024!",
    ]
    
    INVALID_PASSWORDS = [
        "",  # Empty
        "1234567",  # Too short
        "a" * 256,  # Too long
        "  TestPassword123!  ",  # Leading/trailing spaces
    ]
    
    @staticmethod
    def get_password_test_cases() -> Dict[str, list]:
        """Get comprehensive password test cases."""
        return {
            "weak": PasswordTestHelper.WEAK_PASSWORDS,
            "strong": PasswordTestHelper.STRONG_PASSWORDS,
            "invalid": PasswordTestHelper.INVALID_PASSWORDS,
        }


class EmailTestHelper:
    """Helper class for email testing scenarios."""
    
    VALID_EMAILS = [
        "test@example.com",
        "user.name@domain.org",
        "test+tag@example.co.uk",
        "user123@sub.domain.com",
        "test.email.with+symbol@example.com",
    ]
    
    INVALID_EMAILS = [
        "invalid-email",
        "@example.com",
        "test@",
        "test..test@example.com",
        "test@example",
        "test@.com",
        "",  # Empty
        "test@example..com",
    ]
    
    @staticmethod
    def get_email_test_cases() -> Dict[str, list]:
        """Get comprehensive email test cases."""
        return {
            "valid": EmailTestHelper.VALID_EMAILS,
            "invalid": EmailTestHelper.INVALID_EMAILS,
        }


class APITestHelper:
    """Helper class for API testing utilities."""
    
    @staticmethod
    def assert_error_response(
        response_data: Dict[str, Any],
        expected_code: str,
        expected_status: str = "error"
    ):
        """Assert error response format and content."""
        assert "error" in response_data
        assert "status" in response_data
        assert response_data["status"] == expected_status
        assert response_data["error"]["code"] == expected_code
        assert "message" in response_data["error"]
        assert "error_id" in response_data["error"]
    
    @staticmethod
    def assert_success_response(
        response_data: Dict[str, Any],
        expected_status: str = "success"
    ):
        """Assert success response format."""
        if "status" in response_data:
            assert response_data["status"] == expected_status
    
    @staticmethod
    def assert_user_response(response_data: Dict[str, Any], user: User):
        """Assert user response contains expected user data."""
        assert "id" in response_data
        assert "email" in response_data
        assert "full_name" in response_data
        assert "is_active" in response_data
        assert "created_at" in response_data
        assert "updated_at" in response_data
        
        assert response_data["email"] == user.email
        assert response_data["full_name"] == user.full_name
        assert response_data["is_active"] == user.is_active
        
        # Ensure sensitive data is not included
        assert "hashed_password" not in response_data
        assert "password" not in response_data
    
    @staticmethod
    def assert_token_response(response_data: Dict[str, Any]):
        """Assert token response contains expected token data."""
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "token_type" in response_data
        assert "expires_in" in response_data
        
        assert response_data["token_type"] == "bearer"
        assert isinstance(response_data["expires_in"], int)
        assert response_data["expires_in"] > 0


class RateLimitTestHelper:
    """Helper class for rate limiting tests."""
    
    @staticmethod
    def exhaust_rate_limit(
        client: TestClient,
        endpoint: str,
        payload: Dict[str, Any],
        limit: int = 3
    ) -> list:
        """
        Make requests until rate limit is hit.
        Returns list of response status codes.
        """
        responses = []
        for _ in range(limit + 1):  # One more than limit to trigger rate limiting
            response = client.post(endpoint, json=payload)
            responses.append(response.status_code)
        return responses
    
    @staticmethod
    def assert_rate_limit_response(response_data: Dict[str, Any]):
        """Assert rate limit error response format."""
        APITestHelper.assert_error_response(response_data, "RATE_LIMIT_EXCEEDED")
        assert "details" in response_data["error"]
        assert "retry_after" in response_data["error"]["details"]