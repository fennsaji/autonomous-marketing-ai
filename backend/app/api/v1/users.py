"""
User management API endpoints.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserStatistics

router = APIRouter(prefix="/users")


@router.get("/profile", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return UserResponse.from_orm(current_user)


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile."""
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse.from_orm(current_user)


@router.get("/statistics", response_model=UserStatistics)
async def get_user_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user statistics and usage metrics."""
    # TODO: Implement statistics calculation
    return UserStatistics(
        account_age_days=0,
        total_posts_created=0,
        total_posts_published=0,
        total_ai_generations={"captions": 0, "images": 0, "hashtags": 0},
        spending={"total_ai_cost_cents": 0, "monthly_cost_cents": 0},
        performance={"avg_engagement_rate": 0.0}
    )