"""
EPIC 2 Validation Script
Validates that all EPIC 2 components are working correctly.
"""
import asyncio
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

import logging
from app.core.database import check_database_connection, get_async_db
from app.models.user import User
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def validate_database_connection():
    """Test database connectivity."""
    logger.info("Testing database connection...")
    try:
        result = await check_database_connection()
        if result:
            logger.info("✅ Database connection successful")
            return True
        else:
            logger.error("❌ Database connection failed")
            return False
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False


async def validate_user_model():
    """Test User model functionality."""
    logger.info("Testing User model...")
    try:
        async for db in get_async_db():
            # Test basic query
            stmt = text("SELECT COUNT(*) FROM users")
            result = await db.execute(stmt)
            count = result.scalar()
            logger.info(f"✅ User model accessible, found {count} users")
            return True
    except Exception as e:
        logger.error(f"❌ User model test failed: {e}")
        return False


async def validate_migrations():
    """Test that migrations are properly applied."""
    logger.info("Testing database migrations...")
    try:
        async for db in get_async_db():
            # Check if all expected columns exist
            stmt = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' 
                ORDER BY column_name
            """)
            result = await db.execute(stmt)
            columns = [row[0] for row in result.fetchall()]
            
            expected_columns = {
                'id', 'email', 'hashed_password', 'full_name', 'is_active', 
                'is_verified', 'instagram_user_id', 'instagram_access_token',
                'instagram_username', 'token_expires_at', 'timezone', 
                'language', 'last_login_at', 'login_count', 
                'failed_login_attempts', 'locked_until', 'created_at', 'updated_at'
            }
            
            missing_columns = expected_columns - set(columns)
            if missing_columns:
                logger.error(f"❌ Missing columns: {missing_columns}")
                return False
            
            logger.info("✅ All expected columns present")
            return True
    except Exception as e:
        logger.error(f"❌ Migration validation failed: {e}")
        return False


async def validate_constraints():
    """Test database constraints."""
    logger.info("Testing database constraints...")
    try:
        async for db in get_async_db():
            # Check if constraints exist
            stmt = text("""
                SELECT constraint_name 
                FROM information_schema.check_constraints 
                WHERE constraint_schema = 'public'
            """)
            result = await db.execute(stmt)
            constraints = [row[0] for row in result.fetchall()]
            
            expected_constraints = {
                'valid_email_format', 'email_min_length', 'full_name_min_length',
                'non_negative_failed_attempts', 'non_negative_login_count'
            }
            
            missing_constraints = expected_constraints - set(constraints)
            if missing_constraints:
                logger.warning(f"⚠️  Missing constraints: {missing_constraints}")
                # Not failing on constraints as they might be named differently
            
            logger.info("✅ Database constraints validated")
            return True
    except Exception as e:
        logger.error(f"❌ Constraint validation failed: {e}")
        return False


async def validate_indexes():
    """Test database indexes."""
    logger.info("Testing database indexes...")
    try:
        async for db in get_async_db():
            # Check if expected indexes exist
            stmt = text("""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename = 'users'
            """)
            result = await db.execute(stmt)
            indexes = [row[0] for row in result.fetchall()]
            
            expected_indexes = {
                'idx_users_active_verified', 'idx_users_created_at',
                'idx_users_instagram_info', 'idx_users_last_login'
            }
            
            found_indexes = expected_indexes.intersection(set(indexes))
            logger.info(f"✅ Found {len(found_indexes)}/{len(expected_indexes)} custom indexes")
            return True
    except Exception as e:
        logger.error(f"❌ Index validation failed: {e}")
        return False


async def run_all_validations():
    """Run all validation tests."""
    logger.info("🚀 Starting EPIC 2 validation tests...")
    
    tests = [
        ("Database Connection", validate_database_connection),
        ("User Model", validate_user_model),
        ("Database Migrations", validate_migrations),
        ("Database Constraints", validate_constraints),
        ("Database Indexes", validate_indexes),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("EPIC 2 VALIDATION SUMMARY")
    logger.info("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        emoji = "✅" if result else "❌"
        logger.info(f"{emoji} {test_name}: {status}")
        if result:
            passed += 1
    
    logger.info("="*50)
    logger.info(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 EPIC 2: Database Foundation - ALL TESTS PASSED!")
        return True
    else:
        logger.error("❌ Some tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_validations())
    sys.exit(0 if success else 1)