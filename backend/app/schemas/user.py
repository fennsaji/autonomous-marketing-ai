"""
User-related Pydantic schemas.
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    full_name: Optional[str] = None
    bio: Optional[str] = None
    timezone: str = "UTC"


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        
        return v


class UserUpdate(BaseModel):
    """Schema for user updates."""
    full_name: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    notification_preferences: Optional[Dict[str, Any]] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: str
    is_active: bool
    is_verified: bool
    instagram_connected: bool
    instagram_username: Optional[str] = None
    notification_preferences: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class UserStatistics(BaseModel):
    """Schema for user statistics."""
    account_age_days: int
    total_posts_created: int
    total_posts_published: int
    total_ai_generations: Dict[str, int]  # {"captions": 145, "images": 67, "hashtags": 89}
    spending: Dict[str, int]  # {"total_ai_cost_cents": 2450, "monthly_cost_cents": 380}
    performance: Dict[str, float]  # Various performance metrics
    
    model_config = {"from_attributes": True}