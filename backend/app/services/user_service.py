"""
User service for authentication and user management operations.
"""
import logging
from typing import Optional
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.auth import UserRegisterRequest, UserLoginRequest
from app.core.auth import hash_password, verify_password, validate_password_strength
from app.utils.exceptions import (
    UserAlreadyExistsError, InvalidCredentialsError, PasswordTooWeakError,
    AccountInactiveError, DatabaseException
)

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserRegisterRequest) -> User:
        """
        Create a new user account.
        
        Args:
            user_data: User registration data
            
        Returns:
            User object
            
        Raises:
            PasswordTooWeakError: If password doesn't meet requirements
            UserAlreadyExistsError: If user already exists
            DatabaseException: If database operation fails
        """
        try:
            # Validate password strength
            is_valid, message = validate_password_strength(user_data.password)
            if not is_valid:
                raise PasswordTooWeakError(message)
            
            # Check if user already exists
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise UserAlreadyExistsError()
            
            # Hash password
            hashed_password = hash_password(user_data.password)
            
            # Create user
            user = User(
                id=str(uuid4()),
                email=user_data.email.lower().strip(),
                hashed_password=hashed_password,
                full_name=user_data.full_name.strip() if user_data.full_name else None,
                is_active=True,
                is_verified=False  # Email verification required
            )
            
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            
            logger.info("Created new user account: %s", user.email)
            return user
            
        except (PasswordTooWeakError, UserAlreadyExistsError):
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("Database integrity error creating user: %s", e)
            raise UserAlreadyExistsError() from e
        except Exception as e:
            await self.db.rollback()
            logger.error("Error creating user: %s", e)
            raise DatabaseException("Failed to create user account") from e
    
    async def authenticate_user(self, login_data: UserLoginRequest) -> User:
        """
        Authenticate user credentials.
        
        Args:
            login_data: User login credentials
            
        Returns:
            User object
            
        Raises:
            InvalidCredentialsError: If credentials are invalid
            AccountInactiveError: If user account is inactive
            DatabaseException: If database operation fails
        """
        try:
            # Get user by email
            user = await self.get_user_by_email(login_data.email)
            if not user:
                raise InvalidCredentialsError()
            
            # Check if user is active
            if not user.is_active:
                raise AccountInactiveError()
            
            # Verify password
            if not verify_password(login_data.password, user.hashed_password):
                logger.warning("Failed login attempt for user: %s", login_data.email)
                raise InvalidCredentialsError()
            
            # Update last login time
            await self.update_last_login(user)
            
            logger.info("User authenticated successfully: %s", user.email)
            return user
            
        except (InvalidCredentialsError, AccountInactiveError):
            raise
        except Exception as e:
            logger.error("Error authenticating user: %s", e)
            raise DatabaseException("Authentication failed") from e
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User email address
            
        Returns:
            User object if found, None otherwise
        """
        try:
            stmt = select(User).where(User.email == email.lower().strip())
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting user by email: %s", e)
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object if found, None otherwise
        """
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error("Error getting user by ID: %s", e)
            return None
    
    async def update_last_login(self, user: User) -> bool:
        """
        Update user's last login timestamp.
        
        Args:
            user: User object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user.last_login_at = datetime.utcnow()
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Error updating last login: %s", e)
            return False
    
    async def activate_user(self, user: User) -> bool:
        """
        Activate user account.
        
        Args:
            user: User object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user.is_active = True
            await self.db.commit()
            logger.info("User account activated: %s", user.email)
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Error activating user: %s", e)
            return False
    
    async def deactivate_user(self, user: User) -> bool:
        """
        Deactivate user account.
        
        Args:
            user: User object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user.is_active = False
            await self.db.commit()
            logger.info("User account deactivated: %s", user.email)
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Error deactivating user: %s", e)
            return False
    
    async def verify_user_email(self, user: User) -> bool:
        """
        Mark user email as verified.
        
        Args:
            user: User object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user.is_verified = True
            await self.db.commit()
            logger.info("User email verified: %s", user.email)
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Error verifying user email: %s", e)
            return False
    
    async def change_password(self, user: User, current_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            user: User object
            current_password: Current password
            new_password: New password
            
        Returns:
            True if successful
            
        Raises:
            InvalidCredentialsError: If current password is incorrect
            PasswordTooWeakError: If new password doesn't meet requirements
            DatabaseException: If database operation fails
        """
        try:
            # Verify current password
            if not verify_password(current_password, user.hashed_password):
                raise InvalidCredentialsError("Current password is incorrect")
            
            # Validate new password strength
            is_valid, message = validate_password_strength(new_password)
            if not is_valid:
                raise PasswordTooWeakError(message)
            
            # Hash new password
            user.hashed_password = hash_password(new_password)
            await self.db.commit()
            
            logger.info("Password changed for user: %s", user.email)
            return True
            
        except (InvalidCredentialsError, PasswordTooWeakError):
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            logger.error("Error changing password: %s", e)
            raise DatabaseException("Failed to change password") from e
    
    async def update_user_profile(self, user: User, full_name: Optional[str] = None) -> bool:
        """
        Update user profile information.
        
        Args:
            user: User object
            full_name: New full name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if full_name is not None:
                user.full_name = full_name.strip() if full_name else None
            
            await self.db.commit()
            logger.info("Profile updated for user: %s", user.email)
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error("Error updating user profile: %s", e)
            return False