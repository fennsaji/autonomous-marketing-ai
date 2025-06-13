"""
Post-related Pydantic schemas.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.post import PostStatus, PostType


class PostBase(BaseModel):
    """Base post schema."""
    caption: str = Field(..., max_length=2200, min_length=1)
    hashtags: List[str] = Field(default=[], max_items=30)
    media_urls: List[str] = Field(..., min_items=1, max_items=10)
    post_type: PostType = PostType.PHOTO
    
    @validator('hashtags')
    def validate_hashtags(cls, v):
        """Validate hashtags format."""
        if v:
            for hashtag in v:
                if not hashtag.startswith('#'):
                    raise ValueError('Hashtags must start with #')
                if len(hashtag) > 50:
                    raise ValueError('Hashtag too long (max 50 characters)')
        return v
    
    @validator('media_urls')
    def validate_media_urls(cls, v):
        """Validate media URLs."""
        if not v:
            raise ValueError('At least one media URL is required')
        
        for url in v:
            if not url.startswith(('http://', 'https://')):
                raise ValueError('Invalid media URL format')
        
        return v


class PostCreate(PostBase):
    """Schema for post creation."""
    campaign_id: Optional[str] = None
    scheduled_time: Optional[datetime] = None


class PostUpdate(BaseModel):
    """Schema for post updates."""
    caption: Optional[str] = Field(None, max_length=2200, min_length=1)
    hashtags: Optional[List[str]] = Field(None, max_items=30)
    media_urls: Optional[List[str]] = Field(None, min_items=1, max_items=10)
    scheduled_time: Optional[datetime] = None
    
    @validator('hashtags')
    def validate_hashtags(cls, v):
        """Validate hashtags format."""
        if v:
            for hashtag in v:
                if not hashtag.startswith('#'):
                    raise ValueError('Hashtags must start with #')
                if len(hashtag) > 50:
                    raise ValueError('Hashtag too long (max 50 characters)')
        return v


class PostAnalytics(BaseModel):
    """Schema for post analytics."""
    likes_count: int
    comments_count: int
    shares_count: int
    saves_count: int
    reach: int
    impressions: int
    engagement_rate: float


class CampaignInfo(BaseModel):
    """Schema for campaign information in post response."""
    id: str
    name: str


class PostResponse(PostBase):
    """Schema for post response."""
    id: str
    status: PostStatus
    scheduled_time: Optional[datetime] = None
    published_at: Optional[datetime] = None
    instagram_post_id: Optional[str] = None
    instagram_permalink: Optional[str] = None
    campaign: Optional[CampaignInfo] = None
    analytics: Optional[PostAnalytics] = None
    ai_prompt: Optional[str] = None
    ai_model_used: Optional[str] = None
    generation_cost: int  # Cost in cents
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostsResponse(BaseModel):
    """Schema for multiple posts response with pagination."""
    posts: List[PostResponse]
    total: int
    page: int
    pages: int
    has_next: bool
    has_prev: bool


class PublishResponse(BaseModel):
    """Schema for post publish response."""
    message: str
    instagram_post_id: str
    published_at: datetime


class PostPerformance(BaseModel):
    """Schema for detailed post performance."""
    post_id: str
    published_at: datetime
    performance_data: PostAnalytics
    audience_insights: Dict[str, Any]
    time_analysis: Dict[str, Any]