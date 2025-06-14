"""
Unit tests for authentication functions.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_password_strength_score,
    validate_password_strength
)
from tests.test_utils import PasswordTestHelper


class TestPasswordHashing:
    """Test password hashing and verification functions."""
    
    @pytest.mark.unit
    def test_hash_password_creates_hash(self) -> None:
        """Test that password hashing creates a hash string."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)
        assert hashed != password
        assert len(hashed) > 0
    
    @pytest.mark.unit
    def test_hash_password_different_hashes(self) -> None:
        """Test that same password creates different hashes (due to salt)."""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2
    
    @pytest.mark.unit
    def test_verify_password_correct(self) -> None:
        """Test password verification with correct password."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    @pytest.mark.unit
    def test_verify_password_incorrect(self) -> None:
        """Test password verification with incorrect password."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    @pytest.mark.unit
    def test_verify_password_empty_password(self):
        """Test password verification with empty password."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert verify_password("", hashed) is False
    
    @pytest.mark.unit
    def test_verify_password_empty_hash(self):
        """Test password verification with empty hash."""
        password = "TestPassword123!"
        
        assert verify_password(password, "") is False


class TestJWTTokens:
    """Test JWT token creation and verification."""
    
    @pytest.mark.unit
    def test_create_access_token(self):
        """Test access token creation."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        token = create_access_token(data={"sub": user_id})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        assert "." in token  # JWT format
    
    @pytest.mark.unit
    def test_create_refresh_token(self):
        """Test refresh token creation."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        token = create_refresh_token(data={"sub": user_id})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        assert "." in token  # JWT format
    
    @pytest.mark.unit
    def test_create_access_token_with_custom_expiry(self):
        """Test access token creation with custom expiry."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        expires_delta = timedelta(hours=1)
        token = create_access_token(data={"sub": user_id}, expires_delta=expires_delta)
        
        payload = verify_token(token, token_type="access")
        assert payload is not None
        assert payload["sub"] == user_id
    
    @pytest.mark.unit
    def test_create_refresh_token_with_custom_expiry(self):
        """Test refresh token creation with custom expiry."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        expires_delta = timedelta(days=1)
        token = create_refresh_token(data={"sub": user_id}, expires_delta=expires_delta)
        
        payload = verify_token(token, token_type="refresh")
        assert payload is not None
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
    
    @pytest.mark.unit
    def test_verify_valid_access_token(self):
        """Test verification of valid access token."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        token = create_access_token(data={"sub": user_id})
        
        payload = verify_token(token, token_type="access")
        assert payload is not None
        assert payload["sub"] == user_id
        assert "exp" in payload
    
    @pytest.mark.unit
    def test_verify_valid_refresh_token(self):
        """Test verification of valid refresh token."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        token = create_refresh_token(data={"sub": user_id})
        
        payload = verify_token(token, token_type="refresh")
        assert payload is not None
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
        assert "exp" in payload
    
    @pytest.mark.unit
    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token, token_type="access")
        assert payload is None
    
    @pytest.mark.unit
    def test_verify_expired_token(self):
        """Test verification of expired token."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        # Create token that expires immediately
        token = create_access_token(
            data={"sub": user_id}, 
            expires_delta=timedelta(seconds=-1)
        )
        
        payload = verify_token(token, token_type="access")
        assert payload is None
    
    @pytest.mark.unit
    def test_verify_access_token_as_refresh(self):
        """Test verification of access token as refresh token (should fail)."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        access_token = create_access_token(data={"sub": user_id})
        
        payload = verify_token(access_token, token_type="refresh")
        assert payload is None
    
    @pytest.mark.unit
    def test_verify_refresh_token_as_access(self):
        """Test verification of refresh token as access token (should pass)."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        refresh_token = create_refresh_token(data={"sub": user_id})
        
        # Refresh tokens can be verified as access tokens
        payload = verify_token(refresh_token, token_type="access")
        assert payload is not None
        assert payload["sub"] == user_id
    
    @pytest.mark.unit
    def test_verify_token_missing_expiry(self):
        """Test verification of token missing expiry claim."""
        with patch('app.core.auth.jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user_id"}  # Missing exp claim
            
            payload = verify_token("fake_token", token_type="access")
            assert payload is None


class TestPasswordStrength:
    """Test password strength validation functions."""
    
    @pytest.mark.unit
    def test_password_strength_score_empty(self):
        """Test password strength score for empty password."""
        score = get_password_strength_score("")
        assert score == 0
    
    @pytest.mark.unit
    def test_password_strength_score_weak(self):
        """Test password strength score for weak passwords."""
        for password in PasswordTestHelper.WEAK_PASSWORDS:
            score = get_password_strength_score(password)
            assert 0 <= score < 60  # Weak passwords should score low
    
    @pytest.mark.unit
    def test_password_strength_score_strong(self):
        """Test password strength score for strong passwords."""
        for password in PasswordTestHelper.STRONG_PASSWORDS:
            score = get_password_strength_score(password)
            assert score >= 60  # Strong passwords should score high
    
    @pytest.mark.unit
    def test_password_strength_score_length_bonus(self):
        """Test password strength score increases with length."""
        password_8 = "Abc123!@"
        password_12 = "Abc123!@MoreChars"
        password_16 = "Abc123!@EvenMoreChars123"
        
        score_8 = get_password_strength_score(password_8)
        score_12 = get_password_strength_score(password_12)
        score_16 = get_password_strength_score(password_16)
        
        assert score_12 > score_8
        assert score_16 > score_12
    
    @pytest.mark.unit
    def test_password_strength_score_character_variety(self):
        """Test password strength score increases with character variety."""
        lower_only = "abcdefghij"
        lower_upper = "AbCdEfGhIj"
        lower_upper_digit = "AbCdEfGh12"
        all_types = "AbCdEfGh12!@"
        
        score_1 = get_password_strength_score(lower_only)
        score_2 = get_password_strength_score(lower_upper)
        score_3 = get_password_strength_score(lower_upper_digit)
        score_4 = get_password_strength_score(all_types)
        
        assert score_2 > score_1
        assert score_3 > score_2
        assert score_4 > score_3
    
    @pytest.mark.unit
    @patch('app.core.auth.settings')
    def test_validate_password_strength_too_short(self, mock_settings):
        """Test password validation for too short password."""
        mock_settings.PASSWORD_MIN_LENGTH = 8
        mock_settings.PASSWORD_MAX_LENGTH = 128
        mock_settings.PASSWORD_STRENGTH_THRESHOLD = 60
        
        is_valid, message = validate_password_strength("short")
        assert is_valid is False
        assert "at least 8 characters" in message
    
    @pytest.mark.unit
    @patch('app.core.auth.settings')
    def test_validate_password_strength_too_long(self, mock_settings):
        """Test password validation for too long password."""
        mock_settings.PASSWORD_MIN_LENGTH = 8
        mock_settings.PASSWORD_MAX_LENGTH = 64
        mock_settings.PASSWORD_STRENGTH_THRESHOLD = 60
        
        long_password = "a" * 65
        is_valid, message = validate_password_strength(long_password)
        assert is_valid is False
        assert "less than 64 characters" in message
    
    @pytest.mark.unit
    @patch('app.core.auth.settings')
    def test_validate_password_strength_insufficient_variety(self, mock_settings):
        """Test password validation for insufficient character variety."""
        mock_settings.PASSWORD_MIN_LENGTH = 8
        mock_settings.PASSWORD_MAX_LENGTH = 128
        mock_settings.PASSWORD_STRENGTH_THRESHOLD = 60
        
        # Only lowercase letters
        is_valid, message = validate_password_strength("abcdefghij")
        assert is_valid is False
        assert "at least 3 of the following" in message
    
    @pytest.mark.unit
    @patch('app.core.auth.settings')
    def test_validate_password_strength_weak_score(self, mock_settings):
        """Test password validation for weak password score."""
        mock_settings.PASSWORD_MIN_LENGTH = 8
        mock_settings.PASSWORD_MAX_LENGTH = 128
        mock_settings.PASSWORD_STRENGTH_THRESHOLD = 80
        
        # Password that meets basic requirements but is weak
        is_valid, message = validate_password_strength("Password1!")
        assert is_valid is False
        assert "too weak" in message
        assert "score:" in message
    
    @pytest.mark.unit
    @patch('app.core.auth.settings')
    def test_validate_password_strength_valid(self, mock_settings):
        """Test password validation for valid password."""
        mock_settings.PASSWORD_MIN_LENGTH = 8
        mock_settings.PASSWORD_MAX_LENGTH = 128
        mock_settings.PASSWORD_STRENGTH_THRESHOLD = 60
        
        is_valid, message = validate_password_strength("TestPassword123!")
        assert is_valid is True
        assert "meets security requirements" in message
    
    @pytest.mark.unit
    def test_password_strength_edge_cases(self):
        """Test password strength calculation edge cases."""
        # Test with special characters only
        special_only = "!@#$%^&*()"
        score = get_password_strength_score(special_only)
        assert score >= 0
        
        # Test with numbers only
        numbers_only = "1234567890"
        score = get_password_strength_score(numbers_only)
        assert score >= 0
        
        # Test with very long password
        very_long = "a" * 100
        score = get_password_strength_score(very_long)
        assert score <= 100


class TestAuthUtilitiesErrorHandling:
    """Test error handling in authentication utilities."""
    
    @pytest.mark.unit
    def test_hash_password_with_none(self):
        """Test hash_password with None input."""
        with pytest.raises((TypeError, AttributeError)):
            hash_password(None)
    
    @pytest.mark.unit
    def test_verify_password_with_none(self):
        """Test verify_password with None inputs."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        # These should not crash but return False
        assert verify_password(None, hashed) is False
        assert verify_password(password, None) is False
        assert verify_password(None, None) is False
    
    @pytest.mark.unit
    def test_verify_token_with_none(self):
        """Test verify_token with None input."""
        payload = verify_token(None, token_type="access")
        assert payload is None
    
    @pytest.mark.unit
    def test_verify_token_with_empty_string(self):
        """Test verify_token with empty string."""
        payload = verify_token("", token_type="access")
        assert payload is None
    
    @pytest.mark.unit
    def test_get_password_strength_score_with_none(self):
        """Test get_password_strength_score with None input."""
        with pytest.raises((TypeError, AttributeError)):
            get_password_strength_score(None)
    
    @pytest.mark.unit
    def test_validate_password_strength_with_none(self):
        """Test validate_password_strength with None input."""
        with pytest.raises((TypeError, AttributeError)):
            validate_password_strength(None)