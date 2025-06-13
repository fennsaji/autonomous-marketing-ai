"""
AI content generation Pydantic schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class CaptionGenerateRequest(BaseModel):
    """Schema for caption generation request."""
    product_description: str = Field(..., max_length=1000, min_length=1)
    tone: str = Field(default="professional")  # "professional", "casual", "luxury"
    style: str = Field(default="engaging")     # "engaging", "informative", "promotional"
    include_hashtags: bool = Field(default=True)
    max_length: int = Field(default=1500, ge=100, le=2200)
    target_audience: Optional[str] = Field(None)  # "young_professionals", "families", etc.
    call_to_action: Optional[str] = Field(None)   # "shop_now", "learn_more", etc.


class CaptionResponse(BaseModel):
    """Schema for caption generation response."""
    caption: str
    word_count: int
    character_count: int
    hashtags_included: int
    model_used: str
    tokens_used: int
    cost_cents: int
    generation_time_ms: int


class ImageGenerateRequest(BaseModel):
    """Schema for image generation request."""
    prompt: str = Field(..., max_length=1000, min_length=1)
    style: str = Field(default="photorealistic")  # "photorealistic", "artistic", "minimalist"
    quality: str = Field(default="hd")             # "standard", "hd"
    size: str = Field(default="1024x1024")         # "1024x1024", "1024x1792", "1792x1024"
    lighting: Optional[str] = Field(None)          # "natural", "studio", "dramatic"
    background: Optional[str] = Field(None)        # "clean_minimalist", "home_setting", "outdoor"


class ImageResponse(BaseModel):
    """Schema for image generation response."""
    image_url: str
    prompt_used: str
    model_used: str
    size: str
    quality: str
    cost_cents: int
    generation_time_ms: int
    expires_at: str  # ISO timestamp when the URL expires


class HashtagSuggestionRequest(BaseModel):
    """Schema for hashtag suggestion request."""
    content_description: str = Field(..., max_length=500, min_length=1)
    niche: str = Field(default="home_decor")
    count: int = Field(default=15, ge=5, le=30)
    competition_level: str = Field(default="medium")  # "low", "medium", "high"
    include_branded: bool = Field(default=True)


class CompetitionAnalysis(BaseModel):
    """Schema for hashtag competition analysis."""
    low_competition: int
    medium_competition: int
    high_competition: int


class EstimatedReach(BaseModel):
    """Schema for estimated reach."""
    min: int
    max: int


class HashtagResponse(BaseModel):
    """Schema for hashtag suggestion response."""
    hashtags: List[str]
    total_count: int
    competition_analysis: CompetitionAnalysis
    estimated_reach: EstimatedReach


class ContentAnalysisRequest(BaseModel):
    """Schema for content performance analysis request."""
    posts_data: List[Dict]
    time_period: str = Field(default="last_30_days")


class ContentAnalysisResponse(BaseModel):
    """Schema for content analysis response."""
    analysis: Dict
    recommendations: List[str]
    model_used: str
    tokens_used: int
    cost_cents: int