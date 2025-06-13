"""
Post model for Instagram content management.
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime
from enum import Enum


class PostStatus(str, Enum):
    """Post status enumeration."""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class PostType(str, Enum):
    """Post type enumeration."""
    PHOTO = "photo"
    VIDEO = "video"
    CAROUSEL = "carousel"
    REEL = "reel"


class Post(Base):
    """Post model for storing Instagram content."""
    
    __tablename__ = "posts"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=True, index=True)
    
    # Content details
    caption = Column(Text, nullable=False)
    hashtags = Column(ARRAY(String(50)), default=[])
    media_urls = Column(ARRAY(Text), nullable=False)  # Array for carousel posts
    post_type = Column(String(20), default=PostType.PHOTO, nullable=False)
    
    # Scheduling and publishing
    scheduled_time = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    status = Column(String(20), default=PostStatus.DRAFT, nullable=False, index=True)
    
    # Instagram data
    instagram_post_id = Column(String(100), unique=True, index=True, nullable=True)
    instagram_permalink = Column(Text, nullable=True)
    
    # AI generation metadata
    ai_prompt = Column(Text, nullable=True)
    ai_model_used = Column(String(50), nullable=True)
    generation_cost = Column(Integer, default=0)  # Cost in cents
    
    # Analytics data (cached from Instagram API)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    saves_count = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="posts")
    campaign = relationship("Campaign", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, status={self.status}, type={self.post_type})>"
    
    @property
    def is_published(self) -> bool:
        """Check if post is published."""
        return self.status == PostStatus.PUBLISHED
    
    @property
    def is_scheduled(self) -> bool:
        """Check if post is scheduled."""
        return self.status == PostStatus.SCHEDULED and self.scheduled_time is not None
    
    @property
    def total_engagement(self) -> int:
        """Calculate total engagement count."""
        return (
            self.likes_count + 
            self.comments_count + 
            self.shares_count + 
            self.saves_count
        )
    
    @property
    def caption_preview(self) -> str:
        """Get caption preview (first 100 characters)."""
        if not self.caption:
            return ""
        return self.caption[:100] + "..." if len(self.caption) > 100 else self.caption