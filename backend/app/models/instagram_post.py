"""
Instagram post database model.
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from datetime import datetime

from app.core.database import Base


class InstagramPost(Base):
    """Model for tracking published Instagram posts."""
    
    __tablename__ = "instagram_posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Instagram API data
    instagram_post_id = Column(String(100), unique=True, nullable=False, index=True)
    instagram_permalink = Column(Text)
    post_type = Column(String(20), nullable=False)  # 'IMAGE', 'VIDEO', 'CAROUSEL_ALBUM'
    
    # Content data
    caption = Column(Text)
    hashtags = Column(ARRAY(String))  # Array of hashtags
    media_url = Column(Text, nullable=False)
    
    # Publishing metadata
    published_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    api_response = Column(JSON)  # Store full API response for debugging
    
    # Status tracking
    is_published = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="instagram_posts")
    
    def __repr__(self):
        return f"<InstagramPost(id={self.id}, instagram_post_id={self.instagram_post_id}, user_id={self.user_id})>"