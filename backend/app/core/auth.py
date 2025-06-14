"""
Authentication utilities for password hashing and JWT token management.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Stored hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time (default: 7 days)
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    
    logger.info("Created access token for user: %s", data.get("sub"))
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time (default: 30 days)
        
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    
    logger.info("Created refresh token for user: %s", data.get("sub"))
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        token_type: Type of token ("access" or "refresh")
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type for refresh tokens
        if token_type == "refresh":
            if payload.get("type") != "refresh":
                logger.warning("Invalid token type: expected refresh, got %s", payload.get("type"))
                return None
        
        # Check expiration
        exp = payload.get("exp")
        if exp is None:
            logger.warning("Token missing expiration claim")
            return None
        
        if datetime.utcnow() > datetime.fromtimestamp(exp):
            logger.warning("Token has expired")
            return None
        
        return payload
        
    except JWTError as e:
        logger.warning("JWT verification failed: %s", e)
        return None


def get_password_strength_score(password: str) -> int:
    """
    Calculate password strength score (0-100).
    
    Args:
        password: Password to evaluate
        
    Returns:
        Strength score from 0 (weak) to 100 (strong)
    """
    score = 0
    
    # Length scoring
    length = len(password)
    if length >= 8:
        score += 25
    if length >= 12:
        score += 15
    if length >= 16:
        score += 10
    
    # Character variety scoring
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    char_variety = sum([has_lower, has_upper, has_digit, has_special])
    score += char_variety * 12.5  # 50 points max for all 4 types
    
    return min(score, 100)


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password meets security requirements.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        return False, f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long"
    
    if len(password) > settings.PASSWORD_MAX_LENGTH:
        return False, f"Password must be less than {settings.PASSWORD_MAX_LENGTH} characters long"
    
    # Check for at least 3 of 4 character types
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    char_types = sum([has_lower, has_upper, has_digit, has_special])
    if char_types < 3:
        return False, (
            "Password must contain at least 3 of the following: "
            "lowercase letters, uppercase letters, numbers, special characters"
        )
    
    # Check password strength score
    strength_score = get_password_strength_score(password)
    if strength_score < settings.PASSWORD_STRENGTH_THRESHOLD:
        return False, f"Password is too weak (score: {strength_score}/{settings.PASSWORD_STRENGTH_THRESHOLD}). Please choose a stronger password"
    
    return True, "Password meets security requirements"