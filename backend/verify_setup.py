#!/usr/bin/env python3
"""
Verification script to test Epic 1 implementation.
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from app.models.user import User
        from app.schemas.user import UserCreate, UserResponse
        from app.schemas.common import ErrorResponse, HealthResponse
        from app.core.database import create_tables, Base
        from app.api.v1.router import api_router
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_user_model():
    """Test User model creation."""
    try:
        from app.models.user import User
        from app.core.database import Base
        
        # Check if User is properly registered with Base
        assert 'users' in Base.metadata.tables
        table = Base.metadata.tables['users']
        
        # Check required columns exist
        required_columns = ['id', 'email', 'hashed_password', 'created_at', 'updated_at']
        for col in required_columns:
            assert col in table.columns, f"Missing column: {col}"
        
        print("✅ User model validation passed")
        return True
    except Exception as e:
        print(f"❌ User model error: {e}")
        return False

def test_alembic_setup():
    """Test Alembic configuration."""
    try:
        import alembic
        assert os.path.exists('alembic.ini')
        assert os.path.exists('alembic/env.py')
        assert os.path.exists('alembic/versions')
        
        # Check for migration files
        versions_dir = 'alembic/versions'
        migration_files = [f for f in os.listdir(versions_dir) if f.endswith('.py') and f != '__pycache__']
        assert len(migration_files) > 0, "No migration files found"
        
        print("✅ Alembic setup validation passed")
        return True
    except Exception as e:
        print(f"❌ Alembic setup error: {e}")
        return False

def test_api_structure():
    """Test API structure."""
    try:
        from app.api.v1.router import api_router
        from app.core.config import settings
        
        # Check API_V1_STR is defined
        assert hasattr(settings, 'API_V1_STR')
        
        # Check router exists and has routes
        assert len(api_router.routes) > 0
        
        print("✅ API structure validation passed")
        return True
    except Exception as e:
        print(f"❌ API structure error: {e}")
        return False

def test_schemas():
    """Test Pydantic schemas."""
    try:
        from app.schemas.user import UserCreate, UserResponse
        from app.schemas.common import ErrorResponse, HealthResponse
        
        # Test UserCreate schema
        user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        user_create = UserCreate(**user_data)
        assert user_create.email == "test@example.com"
        
        print("✅ Schemas validation passed")
        return True
    except Exception as e:
        print(f"❌ Schemas error: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🔍 Verifying Epic 1 Implementation...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_user_model,
        test_alembic_setup,
        test_api_structure,
        test_schemas
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Epic 1 requirements implemented successfully!")
        return 0
    else:
        print("⚠️  Some issues need to be addressed")
        return 1

if __name__ == "__main__":
    sys.exit(main())