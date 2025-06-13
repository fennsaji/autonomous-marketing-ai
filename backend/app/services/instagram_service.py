"""
Instagram API service for managing Instagram integration.
"""
import httpx
import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

from app.core.config import settings
from app.utils.exceptions import InstagramAPIException, RateLimitException

logger = logging.getLogger(__name__)


class InstagramService:
    """Service for Instagram API operations."""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self.base_url = settings.INSTAGRAM_BASE_URL
        self.rate_limit_remaining = settings.INSTAGRAM_RATE_LIMIT
        self.rate_limit_reset = datetime.utcnow() + timedelta(hours=1)
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """Make authenticated request to Instagram API with rate limiting."""
        
        # Check rate limits
        if self.rate_limit_remaining <= 5:
            if datetime.utcnow() < self.rate_limit_reset:
                wait_time = (self.rate_limit_reset - datetime.utcnow()).total_seconds()
                logger.warning(f"Rate limit approaching, waiting {wait_time} seconds")
                raise RateLimitException(
                    detail=f"Instagram API rate limit exceeded. Try again in {int(wait_time)} seconds.",
                    retry_after=int(wait_time)
                )
        
        url = f"{self.base_url}/{endpoint}"
        request_params = {"access_token": self.access_token}
        
        if params:
            request_params.update(params)
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, params=request_params)
                elif method.upper() == "POST":
                    response = await client.post(url, params=request_params, json=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Update rate limit info
                self.rate_limit_remaining -= 1
                
                response.raise_for_status()
                result = response.json()
                
                # Check for API errors
                if "error" in result:
                    error_message = result["error"].get("message", "Unknown Instagram API error")
                    logger.error(f"Instagram API error: {error_message}")
                    raise InstagramAPIException(error_message)
                
                return result
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    raise RateLimitException("Instagram API rate limit exceeded")
                elif e.response.status_code in [400, 401, 403]:
                    try:
                        error_data = e.response.json()
                        error_message = error_data.get("error", {}).get("message", "Instagram API error")
                    except:
                        error_message = f"Instagram API error: {e.response.status_code}"
                    raise InstagramAPIException(error_message)
                else:
                    raise InstagramAPIException(f"HTTP {e.response.status_code}: {e.response.text}")
            
            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                raise InstagramAPIException("Failed to connect to Instagram API")
    
    async def exchange_auth_code(self, auth_code: str) -> Dict:
        """Exchange authorization code for access token."""
        url = f"{self.base_url}/oauth/access_token"
        
        data = {
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": settings.INSTAGRAM_REDIRECT_URI,
            "code": auth_code
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, data=data)
                response.raise_for_status()
                token_data = response.json()
                
                # Calculate expiration time
                expires_in = token_data.get("expires_in", 3600)
                expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                
                return {
                    "access_token": token_data["access_token"],
                    "token_type": token_data.get("token_type", "bearer"),
                    "expires_at": expires_at,
                    "expires_in": expires_in
                }
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Token exchange failed: {e.response.text}")
                raise InstagramAPIException("Failed to exchange authorization code")
    
    async def get_user_profile(self, access_token: str = None) -> Dict:
        """Get Instagram user profile information."""
        token = access_token or self.access_token
        if not token:
            raise InstagramAPIException("No access token provided")
        
        # Temporarily set token for this request
        original_token = self.access_token
        self.access_token = token
        
        try:
            params = {
                "fields": "id,username,account_type,media_count"
            }
            result = await self._make_request("GET", "me", params=params)
            return result
            
        finally:
            # Restore original token
            self.access_token = original_token
    
    async def upload_photo(
        self, 
        image_url: str, 
        caption: str,
        is_published: bool = True
    ) -> Dict:
        """Upload a photo to Instagram."""
        
        if not self.access_token:
            raise InstagramAPIException("Instagram access token required")
        
        # Step 1: Create media object
        endpoint = "me/media"
        media_data = {
            "image_url": image_url,
            "caption": caption,
            "published": str(is_published).lower()
        }
        
        media_response = await self._make_request("POST", endpoint, data=media_data)
        
        if is_published:
            return media_response
        
        # Step 2: Publish media (if not published in step 1)
        media_id = media_response["id"]
        publish_endpoint = "me/media_publish"
        publish_data = {"creation_id": media_id}
        
        return await self._make_request("POST", publish_endpoint, data=publish_data)
    
    async def upload_video(
        self, 
        video_url: str, 
        caption: str,
        is_reel: bool = False
    ) -> Dict:
        """Upload a video or reel to Instagram."""
        
        if not self.access_token:
            raise InstagramAPIException("Instagram access token required")
        
        endpoint = "me/media"
        media_data = {
            "video_url": video_url,
            "caption": caption,
            "media_type": "REELS" if is_reel else "VIDEO"
        }
        
        # Create media container
        container_response = await self._make_request("POST", endpoint, data=media_data)
        container_id = container_response["id"]
        
        # Wait for video processing
        await self._wait_for_video_processing(container_id)
        
        # Publish video
        publish_data = {"creation_id": container_id}
        return await self._make_request("POST", "me/media_publish", data=publish_data)
    
    async def _wait_for_video_processing(self, container_id: str, max_wait: int = 300):
        """Wait for video processing to complete."""
        start_time = datetime.utcnow()
        
        while (datetime.utcnow() - start_time).total_seconds() < max_wait:
            status_response = await self._make_request(
                "GET", 
                container_id, 
                params={"fields": "status_code"}
            )
            
            status_code = status_response.get("status_code")
            
            if status_code == "FINISHED":
                return True
            elif status_code == "ERROR":
                raise InstagramAPIException("Video processing failed")
            
            # Wait 10 seconds before checking again
            await asyncio.sleep(10)
        
        raise InstagramAPIException("Video processing timeout")
    
    async def get_media_insights(self, media_id: str) -> Dict:
        """Get insights for a specific media post."""
        if not self.access_token:
            raise InstagramAPIException("Instagram access token required")
        
        endpoint = f"{media_id}/insights"
        params = {
            "metric": "impressions,reach,likes,comments,shares,saves"
        }
        return await self._make_request("GET", endpoint, params=params)
    
    async def get_account_insights(
        self, 
        period: str = "day",
        since: Optional[datetime] = None,
        until: Optional[datetime] = None
    ) -> Dict:
        """Get account-level insights."""
        if not self.access_token:
            raise InstagramAPIException("Instagram access token required")
        
        endpoint = "me/insights"
        params = {
            "metric": "impressions,reach,profile_views,follower_count",
            "period": period
        }
        
        if since:
            params["since"] = int(since.timestamp())
        if until:
            params["until"] = int(until.timestamp())
        
        return await self._make_request("GET", endpoint, params=params)
    
    async def refresh_access_token(self) -> Dict:
        """Refresh long-lived access token."""
        if not self.access_token:
            raise InstagramAPIException("Instagram access token required")
        
        endpoint = "oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "fb_exchange_token": self.access_token
        }
        
        result = await self._make_request("GET", endpoint, params=params)
        
        # Calculate new expiration time
        expires_in = result.get("expires_in", 5184000)  # 60 days default
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        return {
            "access_token": result["access_token"],
            "token_type": result.get("token_type", "bearer"),
            "expires_at": expires_at,
            "expires_in": expires_in
        }