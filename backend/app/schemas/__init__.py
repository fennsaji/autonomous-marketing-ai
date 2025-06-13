"""
Pydantic schemas for request/response validation.
"""
from .user import UserCreate, UserResponse, UserUpdate, UserLogin
from .post import PostCreate, PostUpdate, PostResponse, PostsResponse
from .campaign import CampaignCreate, CampaignUpdate, CampaignResponse, CampaignsResponse
from .auth import Token, TokenData
from .content import (
    CaptionGenerateRequest, CaptionResponse,
    ImageGenerateRequest, ImageResponse,
    HashtagSuggestionRequest, HashtagResponse
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserResponse", 
    "UserUpdate",
    "UserLogin",
    
    # Post schemas
    "PostCreate",
    "PostUpdate", 
    "PostResponse",
    "PostsResponse",
    
    # Campaign schemas
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignResponse", 
    "CampaignsResponse",
    
    # Auth schemas
    "Token",
    "TokenData",
    
    # Content generation schemas
    "CaptionGenerateRequest",
    "CaptionResponse",
    "ImageGenerateRequest", 
    "ImageResponse",
    "HashtagSuggestionRequest",
    "HashtagResponse"
]