"""
Test database models.
"""
import pytest
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.models.user import User


@pytest.mark.unit
def test_user_model_creation(db_session: Session):
    """Test creating a user model."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password_here",
        full_name="Test User",
        is_active=True,
        is_verified=False
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert isinstance(user.id, uuid.UUID)
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True
    assert user.is_verified is False
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


@pytest.mark.unit
def test_user_model_required_fields(db_session: Session):
    """Test user model with only required fields."""
    user = User(
        email="minimal@example.com",
        hashed_password="hashed_password_here"
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.email == "minimal@example.com"
    assert user.full_name is None
    assert user.is_active is True  # Default value
    assert user.is_verified is False  # Default value


@pytest.mark.unit
def test_user_model_instagram_fields(db_session: Session):
    """Test user model with Instagram integration fields."""
    user = User(
        email="instagram@example.com",
        hashed_password="hashed_password_here",
        instagram_user_id="12345",
        instagram_access_token="access_token_here"
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.instagram_user_id == "12345"
    assert user.instagram_access_token == "access_token_here"
    assert user.token_expires_at is None


@pytest.mark.unit
def test_user_model_repr(db_session: Session):
    """Test user model string representation."""
    user = User(
        email="repr@example.com",
        hashed_password="hashed_password_here"
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    repr_str = repr(user)
    assert "User" in repr_str
    assert str(user.id) in repr_str
    assert user.email in repr_str