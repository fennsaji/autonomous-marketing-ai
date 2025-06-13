"""
Instagram-related Pydantic schemas.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class InstagramConnect(BaseModel):
    """Schema for Instagram OAuth connection."""
    auth_code: str = Field(..., description="Authorization code from Instagram OAuth")


class InstagramConnectionResponse(BaseModel):
    """Response schema for Instagram connection."""
    message: str
    instagram_user_id: str
    username: str


class InstagramProfileResponse(BaseModel):
    """Instagram profile information response."""
    instagram_user_id: str
    username: str
    account_type: str
    media_count: int
    connected: bool


class InstagramPublishRequest(BaseModel):
    """Request schema for publishing to Instagram."""
    caption: str = Field(..., max_length=2200, description="Post caption")
    hashtags: List[str] = Field(default=[], max_items=30, description="List of hashtags")


class InstagramPublishResponse(BaseModel):
    """Response schema for Instagram publishing."""
    instagram_post_id: str
    success: bool
    message: str
    permalink: Optional[str] = None


class InstagramPreviewRequest(BaseModel):
    """Request schema for post preview."""
    caption: str = Field(..., max_length=2200, description="Post caption")
    hashtags: List[str] = Field(default=[], max_items=30, description="List of hashtags")


class InstagramPreviewResponse(BaseModel):
    """Response schema for post preview."""
    caption: str
    hashtags: List[str]
    character_count: int
    hashtag_count: int
    valid: bool
    warnings: List[str] = []


class InstagramPostStatus(BaseModel):
    """Instagram post status information."""
    post_id: str
    status: str
    permalink: Optional[str] = None
    published_at: Optional[datetime] = None