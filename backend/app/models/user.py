"""
User model for authentication and Instagram integration.
"""
from sqlalchemy import (
    Column, String, Boolean, DateTime, Text, Integer, CheckConstraint, 
    Index, func, text
)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from typing import Optional

from app.core.database import Base


class User(Base):
    """User model with authentication and Instagram integration fields."""
    
    __tablename__ = "users"
    
    # Primary fields
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4, 
        server_default=text('gen_random_uuid()'),
        index=True
    )
    email = Column(
        String(255), 
        unique=True, 
        nullable=False, 
        index=True
    )
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Instagram integration fields (for future sprints)
    instagram_user_id = Column(String(100), unique=True, index=True)
    instagram_access_token = Column(Text)
    instagram_username = Column(String(255))
    token_expires_at = Column(DateTime)
    
    # User preferences and settings
    timezone = Column(String(50), default='UTC', nullable=False)
    language = Column(String(5), default='en', nullable=False)
    
    # Account status tracking
    last_login_at = Column(DateTime)
    login_count = Column(Integer, default=0, nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime)
    
    # Timestamps with proper defaults
    created_at = Column(
        DateTime(timezone=True), 
        default=datetime.utcnow, 
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        server_default=func.now(),
        nullable=False
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'",
            name='valid_email_format'
        ),
        CheckConstraint(
            "char_length(email) >= 5",
            name='email_min_length'
        ),
        CheckConstraint(
            "char_length(full_name) >= 2 OR full_name IS NULL",
            name='full_name_min_length'
        ),
        CheckConstraint(
            "failed_login_attempts >= 0",
            name='non_negative_failed_attempts'
        ),
        CheckConstraint(
            "login_count >= 0",
            name='non_negative_login_count'
        ),
        Index('idx_users_active_verified', 'is_active', 'is_verified'),
        Index('idx_users_instagram_info', 'instagram_user_id', 'instagram_username'),
        Index('idx_users_created_at', 'created_at'),
        Index('idx_users_last_login', 'last_login_at'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, active={self.is_active})>"
    
    @property
    def is_locked(self) -> bool:
        """Check if account is temporarily locked due to failed login attempts."""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    @property
    def has_instagram_connected(self) -> bool:
        """Check if user has connected their Instagram account."""
        return (
            self.instagram_user_id is not None 
            and self.instagram_access_token is not None
        )
    
    @property
    def instagram_token_expired(self) -> bool:
        """Check if Instagram access token has expired."""
        if self.token_expires_at is None:
            return True
        return datetime.utcnow() >= self.token_expires_at