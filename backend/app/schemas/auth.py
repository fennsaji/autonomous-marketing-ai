"""
Authentication schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserRegisterRequest(BaseModel):
    """User registration request schema."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    full_name: Optional[str] = Field(None, max_length=255, description="User's full name")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format and normalize."""
        return v.lower().strip()
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        """Validate and clean full name."""
        if v:
            v = v.strip()
            if len(v) < 2:
                raise ValueError('Full name must be at least 2 characters long')
        return v


class UserLoginRequest(BaseModel):
    """User login request schema."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format and normalize."""
        return v.lower().strip()


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class TokenRefreshRequest(BaseModel):
    """Token refresh request schema."""
    refresh_token: str = Field(..., description="JWT refresh token")


class UserResponse(BaseModel):
    """User response schema."""
    id: UUID = Field(..., description="User's unique identifier")
    email: str = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, description="User's full name")
    is_active: bool = Field(..., description="Whether user account is active")
    is_verified: bool = Field(..., description="Whether user email is verified")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True


class UserRegistrationResponse(BaseModel):
    """User registration response schema."""
    user: UserResponse
    message: str = Field(default="User registered successfully")


class LoginResponse(BaseModel):
    """Login response schema."""
    user: UserResponse
    tokens: TokenResponse
    message: str = Field(default="Login successful")


class LogoutRequest(BaseModel):
    """Logout request schema."""
    refresh_token: Optional[str] = Field(None, description="JWT refresh token to invalidate")


class LogoutResponse(BaseModel):
    """Logout response schema."""
    message: str = Field(default="Logout successful")


class PasswordChangeRequest(BaseModel):
    """Password change request schema."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")


class PasswordStrengthResponse(BaseModel):
    """Password strength validation response."""
    is_valid: bool = Field(..., description="Whether password meets requirements")
    score: int = Field(..., ge=0, le=100, description="Password strength score (0-100)")
    message: str = Field(..., description="Validation message or requirements")


class EmailVerificationRequest(BaseModel):
    """Email verification request schema."""
    token: str = Field(..., description="Email verification token")


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    email: EmailStr = Field(..., description="User's email address")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format and normalize."""
        return v.lower().strip()


class PasswordResetConfirmRequest(BaseModel):
    """Password reset confirmation schema."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")


class AuthErrorResponse(BaseModel):
    """Authentication error response schema."""
    detail: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Specific error code")
    
    
class TokenPayload(BaseModel):
    """JWT token payload schema."""
    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp")
    type: Optional[str] = Field(None, description="Token type (access/refresh)")
    iat: Optional[int] = Field(None, description="Issued at timestamp")
    jti: Optional[str] = Field(None, description="JWT ID for token blacklisting")