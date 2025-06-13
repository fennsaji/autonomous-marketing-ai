"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.security import (
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_user
)
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import Token, InstagramConnect, InstagramConnectionResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.instagram_service import InstagramService
from app.utils.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InstagramAPIException
)

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise UserAlreadyExistsException("Email already registered")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        bio=user_data.bio,
        timezone=user_data.timezone
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse.model_validate(db_user)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return access token."""
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise InvalidCredentialsException("Incorrect email or password")
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "instagram_connected": user.instagram_connected
        }
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse.model_validate(current_user)


@router.post("/instagram/connect", response_model=InstagramConnectionResponse)
async def connect_instagram(
    instagram_data: InstagramConnect,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Connect Instagram account using OAuth authorization code."""
    
    try:
        # Initialize Instagram service
        instagram_service = InstagramService()
        
        # Exchange authorization code for access token
        token_data = await instagram_service.exchange_auth_code(instagram_data.auth_code)
        
        # Get user profile information
        profile_data = await instagram_service.get_user_profile(token_data["access_token"])
        
        # Update user with Instagram credentials
        current_user.instagram_user_id = profile_data["id"]
        current_user.instagram_username = profile_data.get("username")
        current_user.instagram_access_token = token_data["access_token"]
        current_user.token_expires_at = token_data["expires_at"]
        current_user.instagram_connected = True
        
        db.commit()
        
        return InstagramConnectionResponse(
            message="Instagram account connected successfully",
            instagram_user_id=profile_data["id"],
            username=profile_data.get("username", "")
        )
        
    except Exception as e:
        raise InstagramAPIException(f"Failed to connect Instagram account: {str(e)}")


@router.post("/instagram/disconnect")
async def disconnect_instagram(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Disconnect Instagram account."""
    
    # Clear Instagram credentials
    current_user.instagram_user_id = None
    current_user.instagram_username = None
    current_user.instagram_access_token = None
    current_user.token_expires_at = None
    current_user.instagram_connected = False
    
    db.commit()
    
    return {"message": "Instagram account disconnected successfully"}


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Refresh access token."""
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": str(current_user.id),
            "email": current_user.email,
            "full_name": current_user.full_name,
            "instagram_connected": current_user.instagram_connected
        }
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (token invalidation handled client-side)."""
    return {"message": "Successfully logged out"}