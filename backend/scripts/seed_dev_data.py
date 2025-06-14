"""
Development data seeding script.
Creates sample data for development and testing purposes.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.core.database import get_async_db, create_tables
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


async def create_sample_users(db: AsyncSession):
    """Create sample users for development."""
    
    sample_users = [
        {
            "email": "admin@defeah.com",
            "hashed_password": hash_password("admin123"),
            "full_name": "Admin User",
            "is_active": True,
            "is_verified": True,
            "timezone": "UTC",
            "language": "en"
        },
        {
            "email": "demo@defeah.com", 
            "hashed_password": hash_password("demo123"),
            "full_name": "Demo User",
            "is_active": True,
            "is_verified": True,
            "timezone": "America/New_York",
            "language": "en"
        },
        {
            "email": "test@defeah.com",
            "hashed_password": hash_password("test123"),
            "full_name": "Test User",
            "is_active": True,
            "is_verified": False,
            "timezone": "Europe/London",
            "language": "en"
        }
    ]
    
    for user_data in sample_users:
        # Check if user already exists
        from sqlalchemy import select
        stmt = select(User).where(User.email == user_data["email"])
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            logger.info(f"User {user_data['email']} already exists, skipping...")
            continue
            
        # Create new user
        user = User(**user_data)
        db.add(user)
        logger.info(f"Created user: {user_data['email']}")
    
    await db.commit()
    logger.info("Sample users created successfully")


async def seed_development_data():
    """Main function to seed development data."""
    try:
        logger.info("Starting development data seeding...")
        
        # Ensure tables exist
        await create_tables()
        logger.info("Database tables ensured")
        
        # Get database session
        async for db in get_async_db():
            # Create sample users
            await create_sample_users(db)
            break  # Exit after first iteration
            
        logger.info("Development data seeding completed successfully")
        
    except Exception as e:
        logger.error(f"Error seeding development data: {e}")
        raise


async def clear_all_data():
    """Clear all data from the database (use with caution)."""
    try:
        logger.warning("Clearing all data from database...")
        
        async for db in get_async_db():
            # Delete all users
            from sqlalchemy import delete
            await db.execute(delete(User))
            await db.commit()
            break
            
        logger.info("All data cleared successfully")
        
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        raise


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seeding script")
    parser.add_argument(
        "--clear", 
        action="store_true", 
        help="Clear all data before seeding"
    )
    parser.add_argument(
        "--clear-only",
        action="store_true", 
        help="Only clear data, don't seed"
    )
    
    args = parser.parse_args()
    
    async def main():
        if args.clear_only:
            await clear_all_data()
        elif args.clear:
            await clear_all_data()
            await seed_development_data()
        else:
            await seed_development_data()
    
    asyncio.run(main())