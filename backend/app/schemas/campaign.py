"""
Campaign-related Pydantic schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CampaignBase(BaseModel):
    """Base campaign schema."""
    name: str = Field(..., max_length=255, min_length=1)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    posts_per_day: int = Field(default=1, ge=1, le=10)
    content_themes: List[str] = Field(default=[])
    brand_voice: str = Field(default="professional")
    target_hashtags: List[str] = Field(default=[])
    target_reach: Optional[int] = Field(None, ge=0)
    target_engagement_rate: Optional[float] = Field(None, ge=0.0, le=100.0)


class CampaignCreate(CampaignBase):
    """Schema for campaign creation."""
    budget_cents: int = Field(default=0, ge=0)  # Budget in cents


class CampaignUpdate(BaseModel):
    """Schema for campaign updates."""
    name: Optional[str] = Field(None, max_length=255, min_length=1)
    description: Optional[str] = None
    posts_per_day: Optional[int] = Field(None, ge=1, le=10)
    is_active: Optional[bool] = None
    content_themes: Optional[List[str]] = None
    brand_voice: Optional[str] = None
    target_hashtags: Optional[List[str]] = None
    target_reach: Optional[int] = Field(None, ge=0)
    target_engagement_rate: Optional[float] = Field(None, ge=0.0, le=100.0)
    budget_cents: Optional[int] = Field(None, ge=0)


class CampaignPerformance(BaseModel):
    """Schema for campaign performance metrics."""
    total_posts: int
    avg_engagement_rate: float
    total_reach: int
    total_impressions: int


class CampaignResponse(CampaignBase):
    """Schema for campaign response."""
    id: str
    is_active: bool
    budget_cents: int
    spent_cents: int
    performance: Optional[CampaignPerformance] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CampaignsResponse(BaseModel):
    """Schema for multiple campaigns response."""
    campaigns: List[CampaignResponse]
    total: int
    page: int
    pages: int


class CampaignAnalytics(BaseModel):
    """Schema for detailed campaign analytics."""
    campaign_id: str
    period: str
    summary: Dict[str, Any]
    daily_breakdown: List[Dict[str, Any]]
    top_performing_posts: List[Dict[str, Any]]