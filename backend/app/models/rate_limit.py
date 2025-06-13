"""
Instagram rate limiting tracking model.
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.core.database import Base


class InstagramRateLimit(Base):
    """Model for tracking Instagram API rate limits per user."""
    
    __tablename__ = "instagram_rate_limits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Rate limit tracking
    hour_window = Column(DateTime, nullable=False, index=True)  # Hour bucket for rate limiting
    request_count = Column(Integer, default=0, nullable=False)
    last_request = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User")
    
    # Unique constraint for user and hour window
    __table_args__ = (
        UniqueConstraint('user_id', 'hour_window', name='_user_hour_window_uc'),
    )
    
    def __repr__(self):
        return f"<InstagramRateLimit(user_id={self.user_id}, hour_window={self.hour_window}, count={self.request_count})>"