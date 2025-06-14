"""
Database initialization script.
Creates database tables and runs migrations.
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.core.database import create_tables, check_database_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize the database with tables and basic setup."""
    try:
        logger.info("Starting database initialization...")
        
        # Check database connection
        logger.info("Checking database connection...")
        is_healthy = await check_database_connection()
        
        if not is_healthy:
            logger.error("Database connection failed!")
            return False
            
        logger.info("Database connection successful")
        
        # Create tables
        logger.info("Creating database tables...")
        await create_tables()
        logger.info("Database tables created successfully")
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(initialize_database())
    sys.exit(0 if success else 1)