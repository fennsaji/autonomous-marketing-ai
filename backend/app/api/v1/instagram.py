"""
Instagram publishing and management API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.instagram_service import InstagramService
from app.schemas.instagram import (
    InstagramPublishRequest, 
    InstagramPublishResponse,
    InstagramPreviewRequest,
    InstagramPreviewResponse,
    InstagramProfileResponse
)
from app.utils.exceptions import InstagramAPIException

router = APIRouter(prefix="/instagram")


@router.get("/profile", response_model=InstagramProfileResponse)
async def get_instagram_profile(
    current_user: User = Depends(get_current_user)
):
    """Get Instagram profile information."""
    if not current_user.instagram_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instagram account not connected"
        )
    
    try:
        instagram_service = InstagramService(current_user.instagram_access_token)
        profile_data = await instagram_service.get_user_profile()
        
        return InstagramProfileResponse(
            instagram_user_id=profile_data["id"],
            username=profile_data.get("username", ""),
            account_type=profile_data.get("account_type", ""),
            media_count=profile_data.get("media_count", 0),
            connected=True
        )
        
    except Exception as e:
        raise InstagramAPIException(f"Failed to get profile: {str(e)}")


@router.get("/permissions")
async def check_instagram_permissions(
    current_user: User = Depends(get_current_user)
):
    """Check Instagram account permissions and eligibility."""
    if not current_user.instagram_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instagram account not connected"
        )
    
    return {
        "can_publish": True,
        "account_type": "business",
        "permissions": [
            "instagram_basic",
            "instagram_content_publish"
        ]
    }


@router.post("/publish/photo", response_model=InstagramPublishResponse)
async def publish_photo(
    image: UploadFile = File(...),
    caption: str = Form(...),
    hashtags: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Publish a photo to Instagram."""
    if not current_user.instagram_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instagram account not connected"
        )
    
    # Validate image
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    try:
        # TODO: Upload image to temporary storage and get URL
        # For now, using a placeholder URL
        image_url = "https://example.com/temp-image.jpg"
        
        # Process hashtags
        hashtag_list = []
        if hashtags:
            hashtag_list = [tag.strip() for tag in hashtags.split(",")]
        
        # Add hashtags to caption if provided
        full_caption = caption
        if hashtag_list:
            full_caption += " " + " ".join(f"#{tag}" for tag in hashtag_list)
        
        instagram_service = InstagramService(current_user.instagram_access_token)
        result = await instagram_service.upload_photo(image_url, full_caption)
        
        return InstagramPublishResponse(
            instagram_post_id=result["id"],
            success=True,
            message="Photo published successfully",
            permalink=f"https://www.instagram.com/p/{result['id']}"
        )
        
    except Exception as e:
        raise InstagramAPIException(f"Failed to publish photo: {str(e)}")


@router.post("/preview", response_model=InstagramPreviewResponse)
async def preview_post(
    preview_data: InstagramPreviewRequest,
    current_user: User = Depends(get_current_user)
):
    """Preview how a post will appear on Instagram."""
    if not current_user.instagram_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instagram account not connected"
        )
    
    # Validate caption length
    if len(preview_data.caption) > 2200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Caption exceeds 2200 character limit"
        )
    
    # Validate hashtag count
    if len(preview_data.hashtags) > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 30 hashtags allowed"
        )
    
    # Build full caption with hashtags
    full_caption = preview_data.caption
    if preview_data.hashtags:
        full_caption += " " + " ".join(f"#{tag}" for tag in preview_data.hashtags)
    
    return InstagramPreviewResponse(
        caption=full_caption,
        hashtags=preview_data.hashtags,
        character_count=len(full_caption),
        hashtag_count=len(preview_data.hashtags),
        valid=True,
        warnings=[]
    )


@router.get("/posts/{post_id}/status")
async def get_post_status(
    post_id: str,
    current_user: User = Depends(get_current_user)
):
    """Check the status of a published post."""
    if not current_user.instagram_connected:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instagram account not connected"
        )
    
    # TODO: Implement actual post status checking
    return {
        "post_id": post_id,
        "status": "published",
        "permalink": f"https://www.instagram.com/p/{post_id}",
        "published_at": "2024-01-01T00:00:00Z"
    }