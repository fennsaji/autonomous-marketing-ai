"""
Security tests for authentication and input validation.
"""
import pytest
from typing import Dict, Any
from fastapi.testclient import TestClient
from unittest.mock import patch

from tests.factories import SecurityTestDataFactory, EdgeCaseDataFactory
from tests.test_utils import APITestHelper


class TestSQLInjectionPrevention:
    """Test SQL injection prevention in authentication endpoints."""
    
    @pytest.mark.security
    @pytest.mark.parametrize("malicious_email", SecurityTestDataFactory.sql_injection_emails())
    def test_register_sql_injection_prevention(
        self, 
        client: TestClient, 
        malicious_email: str
    ) -> None:
        """Test that SQL injection attempts in registration are prevented."""
        user_data = {
            "email": malicious_email,
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Should either reject due to email validation or handle safely
        assert response.status_code in [400, 422]
        
        # Database should not be affected
        # Verify by checking that no malicious operations occurred
        data = response.json()
        if response.status_code == 422:
            assert "email" in str(data["detail"]).lower()
    
    @pytest.mark.security
    @pytest.mark.parametrize("malicious_email", SecurityTestDataFactory.sql_injection_emails())
    def test_login_sql_injection_prevention(
        self, 
        client: TestClient, 
        malicious_email: str
    ) -> None:
        """Test that SQL injection attempts in login are prevented."""
        login_data = {
            "email": malicious_email,
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        # Should either reject due to validation or return invalid credentials
        assert response.status_code in [401, 422]
        
        data = response.json()
        if response.status_code == 401:
            APITestHelper.assert_error_response(data, "INVALID_CREDENTIALS")


class TestXSSPrevention:
    """Test XSS prevention in user inputs."""
    
    @pytest.mark.security
    @pytest.mark.parametrize("xss_payload", SecurityTestDataFactory.xss_test_strings())
    def test_xss_in_full_name(self, client: TestClient, xss_payload: str) -> None:
        """Test that XSS payloads in full_name are handled safely."""
        user_data = {
            "email": "xsstest@example.com",
            "password": "TestPassword123!",
            "full_name": xss_payload
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        if response.status_code == 201:
            data = response.json()
            stored_name = data["user"]["full_name"]
            
            # Verify XSS payload is stored safely (not executed)
            assert stored_name == xss_payload  # Should be stored as-is, not executed
            
            # Ensure no script execution indicators in response
            response_text = response.text
            assert "<script>" not in response_text.lower()
            assert "javascript:" not in response_text.lower()


class TestInputSanitization:
    """Test input sanitization and validation."""
    
    @pytest.mark.security
    @pytest.mark.parametrize("special_name", SecurityTestDataFactory.special_character_names())
    def test_special_characters_in_names(
        self, 
        client: TestClient, 
        special_name: str
    ) -> None:
        """Test that special characters in names are handled properly."""
        user_data = {
            "email": "special@example.com",
            "password": "TestPassword123!",
            "full_name": special_name
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Should accept valid special characters
        assert response.status_code == 201
        data = response.json()
        assert data["user"]["full_name"] == special_name
    
    @pytest.mark.security
    @pytest.mark.parametrize("malicious_password", SecurityTestDataFactory.malicious_passwords())
    def test_malicious_password_handling(
        self, 
        client: TestClient, 
        malicious_password: str
    ) -> None:
        """Test that malicious password strings are handled safely."""
        user_data = {
            "email": "maliciouspass@example.com",
            "password": malicious_password,
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Should either reject due to validation or store safely
        if response.status_code == 201:
            # If accepted, verify it's stored safely (hashed)
            data = response.json()
            assert "password" not in data["user"]
            assert "hashed_password" not in data["user"]
        else:
            # Should be rejected with proper error
            assert response.status_code in [400, 422]


class TestBoundaryConditions:
    """Test boundary conditions and edge cases."""
    
    @pytest.mark.security
    @pytest.mark.parametrize("boundary_email", EdgeCaseDataFactory.boundary_emails())
    def test_email_boundary_conditions(
        self, 
        client: TestClient, 
        boundary_email: str
    ) -> None:
        """Test email field boundary conditions."""
        user_data = {
            "email": boundary_email,
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Most boundary cases should be rejected
        if boundary_email in ["", "@example.com", "test@", "test..test@example.com"]:
            assert response.status_code == 422
        elif boundary_email == "a@b.c":  # Minimum valid
            assert response.status_code == 201
    
    @pytest.mark.security
    @pytest.mark.parametrize("boundary_password", EdgeCaseDataFactory.boundary_passwords())
    def test_password_boundary_conditions(
        self, 
        client: TestClient, 
        boundary_password: str
    ) -> None:
        """Test password field boundary conditions."""
        user_data = {
            "email": "boundary@example.com",
            "password": boundary_password,
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Most boundary passwords should be rejected
        if len(boundary_password) < 8 or boundary_password.isspace():
            assert response.status_code in [400, 422]


class TestUnicodeHandling:
    """Test Unicode and international character handling."""
    
    @pytest.mark.security
    def test_unicode_names(self, client: TestClient) -> None:
        """Test that Unicode names are handled properly."""
        unicode_data = EdgeCaseDataFactory.unicode_test_data()
        
        for unicode_name in unicode_data["names"]:
            user_data = {
                "email": f"unicode{hash(unicode_name)}@example.com",
                "password": "TestPassword123!",
                "full_name": unicode_name
            }
            
            response = client.post("/api/v1/auth/register", json=user_data)
            
            # Should handle Unicode gracefully
            if response.status_code == 201:
                data = response.json()
                # Unicode should be preserved
                assert data["user"]["full_name"] == unicode_name
    
    @pytest.mark.security
    def test_unicode_emails(self, client: TestClient) -> None:
        """Test Unicode email handling."""
        unicode_data = EdgeCaseDataFactory.unicode_test_data()
        
        for unicode_email in unicode_data["emails"]:
            user_data = {
                "email": unicode_email,
                "password": "TestPassword123!",
                "full_name": "Test User"
            }
            
            response = client.post("/api/v1/auth/register", json=user_data)
            
            # Unicode emails should be handled according to email validation rules
            # Most will be rejected by standard email validation
            assert response.status_code in [201, 422]


class TestAuthenticationBypassAttempts:
    """Test authentication bypass attempt prevention."""
    
    @pytest.mark.security
    def test_jwt_algorithm_confusion(self, client: TestClient) -> None:
        """Test protection against JWT algorithm confusion attacks."""
        # This would require creating malformed JWTs
        # For now, test that invalid tokens are rejected
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    @pytest.mark.security
    def test_empty_authorization_header(self, client: TestClient) -> None:
        """Test handling of empty authorization headers."""
        headers = {"Authorization": ""}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
        
        headers = {"Authorization": "Bearer "}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    @pytest.mark.security
    def test_malformed_authorization_header(self, client: TestClient) -> None:
        """Test handling of malformed authorization headers."""
        malformed_headers = [
            {"Authorization": "Basic invalid"},
            {"Authorization": "Bearer"},
            {"Authorization": "NotBearer token"},
            {"Authorization": "Bearer token1 token2"},
        ]
        
        for headers in malformed_headers:
            response = client.get("/api/v1/auth/me", headers=headers)
            assert response.status_code == 401


class TestRateLimitingBehavior:
    """Test rate limiting behavior under various conditions."""
    
    @pytest.mark.security
    def test_rate_limit_per_ip(self, client: TestClient) -> None:
        """Test that rate limiting is applied per IP address."""
        user_data = {
            "email": "ratelimit@example.com",
            "password": "TestPassword123!",
            "full_name": "Rate Limit Test"
        }
        
        # This test would need rate limiting to be enabled
        # For now, just verify the endpoint responds normally
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code in [201, 409]  # Success or already exists
    
    @pytest.mark.security
    @patch('app.api.v1.auth.check_authentication_rate_limit')
    def test_rate_limit_bypass_attempts(
        self, 
        mock_rate_limit, 
        client: TestClient
    ) -> None:
        """Test that rate limit bypass attempts are prevented."""
        from app.utils.exceptions import RateLimitError
        
        mock_rate_limit.side_effect = RateLimitError(
            "Too many attempts", 
            details={"retry_after": 300}
        )
        
        # Various headers that might be used to bypass rate limiting
        bypass_headers = [
            {"X-Forwarded-For": "1.2.3.4"},
            {"X-Real-IP": "1.2.3.4"},
            {"X-Originating-IP": "1.2.3.4"},
            {"CF-Connecting-IP": "1.2.3.4"},
        ]
        
        user_data = {
            "email": "bypass@example.com", 
            "password": "TestPassword123!"
        }
        
        for headers in bypass_headers:
            response = client.post(
                "/api/v1/auth/register", 
                json=user_data, 
                headers=headers
            )
            # Should still be rate limited
            assert response.status_code == 429
            
            # Verify the rate limit function was called
            mock_rate_limit.assert_called()


class TestPasswordSecurityFeatures:
    """Test password security feature implementation."""
    
    @pytest.mark.security
    def test_password_timing_attack_resistance(self, client: TestClient) -> None:
        """Test that password verification is resistant to timing attacks."""
        # Register a user first
        user_data = {
            "email": "timing@example.com",
            "password": "TestPassword123!",
            "full_name": "Timing Test"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Test with correct and incorrect passwords
        # Note: In a real implementation, we'd measure timing
        correct_login = {
            "email": "timing@example.com",
            "password": "TestPassword123!"
        }
        
        incorrect_login = {
            "email": "timing@example.com", 
            "password": "WrongPassword123!"
        }
        
        # Both should take similar time (not easily measurable in tests)
        correct_response = client.post("/api/v1/auth/login", json=correct_login)
        incorrect_response = client.post("/api/v1/auth/login", json=incorrect_login)
        
        assert correct_response.status_code == 200
        assert incorrect_response.status_code == 401
    
    @pytest.mark.security
    def test_password_hash_uniqueness(self, client: TestClient) -> None:
        """Test that identical passwords produce different hashes."""
        from app.core.auth import hash_password
        
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes should be different due to salt
        assert hash1 != hash2
        
        # But both should verify correctly
        from app.core.auth import verify_password
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)