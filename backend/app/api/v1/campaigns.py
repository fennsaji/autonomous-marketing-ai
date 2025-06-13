"""
Campaign management API endpoints.
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse, CampaignsResponse, CampaignAnalytics
from app.utils.exceptions import CampaignNotFoundException

router = APIRouter(prefix="/campaigns")


@router.get("/", response_model=CampaignsResponse)
async def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's campaigns."""
    query = db.query(Campaign).filter(Campaign.user_id == current_user.id)
    
    if is_active is not None:
        query = query.filter(Campaign.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    campaigns = query.order_by(Campaign.created_at.desc()).offset(skip).limit(limit).all()
    
    # Calculate pagination info
    page = (skip // limit) + 1
    pages = (total + limit - 1) // limit
    
    return CampaignsResponse(
        campaigns=[CampaignResponse.from_orm(campaign) for campaign in campaigns],
        total=total,
        page=page,
        pages=pages
    )


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new campaign."""
    db_campaign = Campaign(
        user_id=current_user.id,
        **campaign_data.dict()
    )
    
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    return CampaignResponse.from_orm(db_campaign)


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific campaign by ID."""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise CampaignNotFoundException("Campaign not found")
    
    return CampaignResponse.from_orm(campaign)


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: str,
    campaign_update: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update existing campaign."""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise CampaignNotFoundException("Campaign not found")
    
    # Update fields
    for field, value in campaign_update.dict(exclude_unset=True).items():
        setattr(campaign, field, value)
    
    db.commit()
    db.refresh(campaign)
    
    return CampaignResponse.from_orm(campaign)


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a campaign."""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise CampaignNotFoundException("Campaign not found")
    
    db.delete(campaign)
    db.commit()
    
    return {"message": "Campaign deleted successfully"}


@router.get("/{campaign_id}/analytics", response_model=CampaignAnalytics)
async def get_campaign_analytics(
    campaign_id: str,
    period: str = Query("last_30_days"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get campaign analytics."""
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id,
        Campaign.user_id == current_user.id
    ).first()
    
    if not campaign:
        raise CampaignNotFoundException("Campaign not found")
    
    # TODO: Implement analytics calculation
    return CampaignAnalytics(
        campaign_id=campaign_id,
        period=period,
        summary={},
        daily_breakdown=[],
        top_performing_posts=[]
    )