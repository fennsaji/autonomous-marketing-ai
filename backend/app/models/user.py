"""
User model for authentication and profile management.
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class User(Base):
    """User model for storing user account information."""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic user information
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    timezone = Column(String(50), default="UTC")
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Instagram account integration
    instagram_user_id = Column(String(100), unique=True, index=True, nullable=True)
    instagram_username = Column(String(100), nullable=True)
    instagram_access_token = Column(Text, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    instagram_connected = Column(Boolean, default=False)
    
    # Notification preferences
    notification_preferences = Column(JSON, default={
        "email_analytics": True,
        "email_post_published": False,
        "push_engagement": True
    })
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")
    instagram_posts = relationship("InstagramPost", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
    
    @property
    def instagram_connected_status(self) -> bool:
        """Check if Instagram account is properly connected."""
        return bool(
            self.instagram_user_id and 
            self.instagram_access_token and 
            self.instagram_connected
        )