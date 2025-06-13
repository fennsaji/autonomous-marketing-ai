"""
Campaign model for managing marketing campaigns.
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class Campaign(Base):
    """Campaign model for organizing marketing campaigns."""
    
    __tablename__ = "campaigns"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Basic campaign information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Campaign timing
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    
    # Content generation settings
    posts_per_day = Column(Integer, default=1)
    content_themes = Column(JSON, default=[])  # e.g., ["modern_living", "cozy_bedroom"]
    brand_voice = Column(String(50), default="professional")  # "professional", "casual", "luxury"
    target_hashtags = Column(JSON, default=[])
    
    # Performance targets
    target_reach = Column(Integer, nullable=True)
    target_engagement_rate = Column(Float, nullable=True)  # Percentage as decimal
    
    # Campaign budget (for AI generation costs)
    budget_cents = Column(Integer, default=0)  # Budget in cents
    spent_cents = Column(Integer, default=0)   # Amount spent in cents
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="campaigns")
    posts = relationship("Post", back_populates="campaign", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Campaign(id={self.id}, name={self.name}, is_active={self.is_active})>"
    
    @property
    def is_running(self) -> bool:
        """Check if campaign is currently running."""
        if not self.is_active:
            return False
        
        now = datetime.utcnow()
        
        # Check start date
        if self.start_date and now < self.start_date:
            return False
        
        # Check end date
        if self.end_date and now > self.end_date:
            return False
        
        return True
    
    @property
    def budget_remaining_cents(self) -> int:
        """Calculate remaining budget in cents."""
        return max(0, self.budget_cents - self.spent_cents)
    
    @property
    def budget_utilization_percentage(self) -> float:
        """Calculate budget utilization percentage."""
        if self.budget_cents == 0:
            return 0.0
        return (self.spent_cents / self.budget_cents) * 100
    
    @property
    def total_posts(self) -> int:
        """Get total number of posts in campaign."""
        return len(self.posts) if self.posts else 0
    
    @property
    def published_posts_count(self) -> int:
        """Get count of published posts."""
        if not self.posts:
            return 0
        return len([post for post in self.posts if post.is_published])
    
    def add_spent_amount(self, amount_cents: int):
        """Add to spent amount."""
        self.spent_cents += amount_cents
        self.updated_at = datetime.utcnow()