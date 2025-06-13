"""
Authentication-related Pydantic schemas.
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class TokenData(BaseModel):
    """Token data schema for internal use."""
    user_id: Optional[str] = None


class InstagramConnect(BaseModel):
    """Schema for Instagram account connection."""
    auth_code: str


class InstagramConnectionResponse(BaseModel):
    """Schema for Instagram connection response."""
    message: str
    instagram_user_id: str
    username: str