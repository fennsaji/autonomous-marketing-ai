"""
Authentication endpoints for user registration, login, and token management.
"""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.core.auth import create_access_token, create_refresh_token, verify_token
from app.core.deps import get_current_user
from app.core.redis_client import token_blacklist
from app.core.rate_limiting import check_authentication_rate_limit
from app.services.user_service import UserService
from app.models.user import User
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    UserRegistrationResponse,
    LoginResponse,
    TokenResponse,
    TokenRefreshRequest,
    UserResponse,
    LogoutRequest,
    LogoutResponse,
    PasswordChangeRequest
)
from app.core.config import settings
from app.utils.exceptions import (
    UserAlreadyExistsError, InvalidCredentialsError, PasswordTooWeakError,
    RateLimitError
)

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserRegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Register a new user account.
    
    Creates a new user with email and password validation.
    Returns user information without authentication tokens.
    Email verification may be required before login.
    """
    # Check rate limit
    try:
        await check_authentication_rate_limit(request, "registration")
    except RateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=e.message,
            headers={"Retry-After": str(e.details.get("retry_after", 300))}
        )
    
    user_service = UserService(db)
    
    try:
        user = await user_service.create_user(user_data)
        
        logger.info("User registered successfully: %s", user.email)
        
        return UserRegistrationResponse(
            user=UserResponse.from_orm(user),
            message="User registered successfully. Please verify your email before logging in."
        )
        
    except (UserAlreadyExistsError, PasswordTooWeakError):
        raise
    except Exception as e:
        logger.error("Error in user registration: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        ) from e


@router.post("/login", response_model=LoginResponse)
async def login_user(
    login_data: UserLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Authenticate user and return access and refresh tokens.
    
    Validates user credentials and returns JWT tokens for API access.
    Tokens can be used for authenticated requests.
    """
    # Check rate limit
    try:
        await check_authentication_rate_limit(request, "login")
    except RateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=e.message,
            headers={"Retry-After": str(e.details.get("retry_after", 60))}
        )
    
    user_service = UserService(db)
    
    try:
        user = await user_service.authenticate_user(login_data)
        
        # Create tokens
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        # Calculate token expiration
        expires_in = settings.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60  # Convert to seconds
        
        logger.info("User logged in successfully: %s", user.email)
        
        return LoginResponse(
            user=UserResponse.from_orm(user),
            tokens=TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=expires_in
            ),
            message="Login successful"
        )
        
    except InvalidCredentialsError:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in user login: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        ) from e


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: TokenRefreshRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Refresh access token using refresh token.
    
    Validates refresh token and returns new access token.
    Refresh token remains valid until expiration.
    """
    try:
        # Verify refresh token
        payload = verify_token(refresh_data.refresh_token, token_type="refresh")
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify user still exists and is active
        user_service = UserService(db)
        user = await user_service.get_user_by_id(user_id)
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Create new access token
        access_token = create_access_token(data={"sub": str(user.id)})
        expires_in = settings.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        
        logger.info("Token refreshed for user: %s", user.email)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_data.refresh_token,  # Return same refresh token
            token_type="bearer",
            expires_in=expires_in
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error refreshing token: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        ) from e


@router.post("/logout", response_model=LogoutResponse)
async def logout_user(
    logout_data: LogoutRequest,
    current_user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Logout user and invalidate tokens.
    
    Blacklists the current access token and optionally the refresh token.
    """
    try:
        # Get the access token from authorization header
        access_token = credentials.credentials
        
        # Calculate TTL for token blacklisting (time until token expires)
        payload = verify_token(access_token, token_type="access")
        if payload:
            exp = payload.get("exp", 0)
            current_time = int(datetime.utcnow().timestamp())
            ttl = max(exp - current_time, 0)
            
            # Blacklist access token
            await token_blacklist.add_token(access_token, ttl)
            logger.info("Access token blacklisted for user: %s", current_user.email)
        
        # Blacklist refresh token if provided
        if logout_data.refresh_token:
            try:
                refresh_payload = verify_token(logout_data.refresh_token, token_type="refresh")
                if refresh_payload:
                    exp = refresh_payload.get("exp", 0)
                    current_time = int(datetime.utcnow().timestamp())
                    ttl = max(exp - current_time, 0)
                    
                    await token_blacklist.add_token(logout_data.refresh_token, ttl)
                    logger.info("Refresh token blacklisted for user: %s", current_user.email)
            except Exception as e:
                logger.warning("Failed to blacklist refresh token: %s", e)
        
        logger.info("User logged out: %s", current_user.email)
        
        return LogoutResponse(
            message="Logout successful"
        )
        
    except Exception as e:
        logger.error("Error during logout: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout"
        ) from e


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user profile information.
    
    Returns authenticated user's profile data.
    Requires valid authentication token.
    """
    try:
        logger.info("Profile accessed by user: %s", current_user.email)
        return UserResponse.from_orm(current_user)
        
    except Exception as e:
        logger.error("Error getting user profile: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error getting profile"
        ) from e


@router.post("/change-password", response_model=dict)
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Change user password.
    
    Validates current password and updates to new password.
    Requires authentication and current password verification.
    """
    user_service = UserService(db)
    
    try:
        await user_service.change_password(
            current_user,
            password_data.current_password,
            password_data.new_password
        )
        
        logger.info("Password changed for user: %s", current_user.email)
        
        return {"message": "Password changed successfully"}
        
    except (InvalidCredentialsError, PasswordTooWeakError):
        raise
    except Exception as e:
        logger.error("Error changing password: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password change"
        ) from e