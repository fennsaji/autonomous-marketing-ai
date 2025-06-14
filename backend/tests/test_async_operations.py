"""
Async database operation tests for comprehensive coverage.
"""
import pytest
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import patch, AsyncMock

from app.models.user import User
from app.services.user_service import UserService
from app.core.auth import hash_password
from tests.factories import UserDataFactory
from tests.test_utils import AuthTestHelper


class TestAsyncUserService:
    """Test async operations in UserService."""
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_user_async(self, async_db_session: AsyncSession) -> None:
        """Test async user creation."""
        user_service = UserService(async_db_session)
        user_data = {
            "email": "async@example.com",
            "password": "TestPassword123!",
            "full_name": "Async User"
        }
        
        from app.schemas.auth import UserRegisterRequest
        register_request = UserRegisterRequest(**user_data)
        
        user = await user_service.create_user(register_request)
        
        assert user.email == user_data["email"]
        assert user.full_name == user_data["full_name"]
        assert user.is_active is True
        assert user.is_verified is False
        assert user.id is not None
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_user_by_email_async(self, async_db_session: AsyncSession) -> None:
        """Test async user retrieval by email."""
        # Create user first
        user = await AuthTestHelper.create_test_user_in_db_async(
            async_db_session,
            email="async_get@example.com",
            password="TestPassword123!"
        )
        
        user_service = UserService(async_db_session)
        retrieved_user = await user_service.get_user_by_email("async_get@example.com")
        
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.email == user.email
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_user_by_id_async(self, async_db_session: AsyncSession) -> None:
        """Test async user retrieval by ID."""
        # Create user first
        user = await AuthTestHelper.create_test_user_in_db_async(
            async_db_session,
            email="async_id@example.com",
            password="TestPassword123!"
        )
        
        user_service = UserService(async_db_session)
        retrieved_user = await user_service.get_user_by_id(str(user.id))
        
        assert retrieved_user is not None
        assert retrieved_user.id == user.id
        assert retrieved_user.email == user.email
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_authenticate_user_async(self, async_db_session: AsyncSession) -> None:
        """Test async user authentication."""
        # Create user first
        password = "TestPassword123!"
        user = await AuthTestHelper.create_test_user_in_db_async(
            async_db_session,
            email="async_auth@example.com",
            password=password,
            is_verified=True
        )
        
        user_service = UserService(async_db_session)
        from app.schemas.auth import UserLoginRequest
        
        login_request = UserLoginRequest(
            email="async_auth@example.com",
            password=password
        )
        
        authenticated_user = await user_service.authenticate_user(login_request)
        
        assert authenticated_user is not None
        assert authenticated_user.id == user.id
        assert authenticated_user.email == user.email
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_change_password_async(self, async_db_session: AsyncSession) -> None:
        """Test async password change."""
        # Create user first
        old_password = "TestPassword123!"
        user = await AuthTestHelper.create_test_user_in_db_async(
            async_db_session,
            email="async_change@example.com",
            password=old_password
        )
        
        user_service = UserService(async_db_session)
        new_password = "NewTestPassword123!"
        
        await user_service.change_password(user, old_password, new_password)
        
        # Verify password was changed
        from app.core.auth import verify_password
        # Refresh user from database
        await async_db_session.refresh(user)
        assert verify_password(new_password, user.hashed_password)
        assert not verify_password(old_password, user.hashed_password)


class TestAsyncDatabaseTransactions:
    """Test async database transaction handling."""
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_rollback_on_error(self, async_db_session: AsyncSession) -> None:
        """Test that database operations are rolled back on error."""
        user_service = UserService(async_db_session)
        
        # Create a user successfully first
        user_data = UserDataFactory()
        from app.schemas.auth import UserRegisterRequest
        register_request = UserRegisterRequest(**user_data)
        
        user = await user_service.create_user(register_request)
        assert user.email == user_data["email"]
        
        # Try to create another user with the same email (should fail)
        duplicate_data = {
            "email": user_data["email"],  # Same email
            "password": "AnotherPassword123!",
            "full_name": "Duplicate User"
        }
        
        duplicate_request = UserRegisterRequest(**duplicate_data)
        
        with pytest.raises(Exception):  # Should raise UserAlreadyExistsError
            await user_service.create_user(duplicate_request)
        
        # Verify original user still exists
        existing_user = await user_service.get_user_by_email(user_data["email"])
        assert existing_user is not None
        assert existing_user.full_name == user_data["full_name"]
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_concurrent_user_creation(self, async_db_session: AsyncSession) -> None:
        """Test concurrent user creation with async operations."""
        import asyncio
        
        user_service = UserService(async_db_session)
        
        async def create_user_async(email: str) -> User:
            user_data = {
                "email": email,
                "password": "TestPassword123!",
                "full_name": f"Concurrent User {email}"
            }
            from app.schemas.auth import UserRegisterRequest
            register_request = UserRegisterRequest(**user_data)
            return await user_service.create_user(register_request)
        
        # Create multiple users concurrently
        emails = [f"concurrent{i}@example.com" for i in range(5)]
        
        tasks = [create_user_async(email) for email in emails]
        users = await asyncio.gather(*tasks)
        
        # All users should be created successfully
        assert len(users) == 5
        for i, user in enumerate(users):
            assert user.email == emails[i]
            assert user.full_name == f"Concurrent User {emails[i]}"


class TestAsyncRedisOperations:
    """Test async Redis operations for token blacklisting."""
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_token_blacklisting_async(self, async_redis_mock) -> None:
        """Test async token blacklisting operations."""
        from app.core.redis_client import TokenBlacklist
        
        # Mock the TokenBlacklist to use our fake Redis
        token_blacklist = TokenBlacklist(async_redis_mock)
        
        token = "test.jwt.token"
        ttl = 3600  # 1 hour
        
        # Add token to blacklist
        await token_blacklist.add_token(token, ttl)
        
        # Verify token is blacklisted
        is_blacklisted = await token_blacklist.is_blacklisted(token)
        assert is_blacklisted is True
        
        # Verify non-blacklisted token
        other_token = "other.jwt.token"
        is_other_blacklisted = await token_blacklist.is_blacklisted(other_token)
        assert is_other_blacklisted is False
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_token_expiration_async(self, async_redis_mock) -> None:
        """Test that blacklisted tokens expire correctly."""
        from app.core.redis_client import TokenBlacklist
        import asyncio
        
        token_blacklist = TokenBlacklist(async_redis_mock)
        
        token = "expiring.jwt.token"
        ttl = 1  # 1 second
        
        # Add token to blacklist with short TTL
        await token_blacklist.add_token(token, ttl)
        
        # Verify token is initially blacklisted
        assert await token_blacklist.is_blacklisted(token) is True
        
        # Wait for expiration
        await asyncio.sleep(1.1)
        
        # Token should no longer be blacklisted
        assert await token_blacklist.is_blacklisted(token) is False


class TestAsyncErrorHandling:
    """Test async error handling and edge cases."""
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_database_connection_error_handling(self) -> None:
        """Test handling of database connection errors."""
        # Create a mock session that raises connection errors
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.execute.side_effect = Exception("Database connection lost")
        
        user_service = UserService(mock_session)
        
        with pytest.raises(Exception) as exc_info:
            await user_service.get_user_by_email("test@example.com")
        
        assert "Database connection lost" in str(exc_info.value)
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_redis_connection_error_handling(self) -> None:
        """Test handling of Redis connection errors."""
        # Create a mock Redis client that raises connection errors
        mock_redis = AsyncMock()
        mock_redis.setex.side_effect = Exception("Redis connection lost")
        
        from app.core.redis_client import TokenBlacklist
        token_blacklist = TokenBlacklist(mock_redis)
        
        with pytest.raises(Exception) as exc_info:
            await token_blacklist.add_token("test.token", 3600)
        
        assert "Redis connection lost" in str(exc_info.value)
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_async_timeout_handling(self, async_db_session: AsyncSession) -> None:
        """Test handling of async operation timeouts."""
        user_service = UserService(async_db_session)
        
        # Mock a slow database operation
        with patch.object(async_db_session, 'execute') as mock_execute:
            async def slow_operation(*args, **kwargs):
                await asyncio.sleep(2)  # Simulate slow operation
                raise asyncio.TimeoutError("Operation timed out")
            
            mock_execute.side_effect = slow_operation
            
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(
                    user_service.get_user_by_email("test@example.com"),
                    timeout=1.0
                )


class TestAsyncServiceIntegration:
    """Test integration between async services."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_full_async_registration_flow(self, async_db_session: AsyncSession) -> None:
        """Test complete async user registration flow."""
        user_service = UserService(async_db_session)
        
        # Step 1: Create user
        user_data = {
            "email": "fullflow@example.com",
            "password": "TestPassword123!",
            "full_name": "Full Flow User"
        }
        
        from app.schemas.auth import UserRegisterRequest
        register_request = UserRegisterRequest(**user_data)
        
        created_user = await user_service.create_user(register_request)
        assert created_user.email == user_data["email"]
        
        # Step 2: Verify user can be retrieved
        retrieved_user = await user_service.get_user_by_email(user_data["email"])
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        
        # Step 3: Verify user can authenticate (after verification)
        # First set user as verified
        retrieved_user.is_verified = True
        await async_db_session.commit()
        
        from app.schemas.auth import UserLoginRequest
        login_request = UserLoginRequest(
            email=user_data["email"],
            password=user_data["password"]
        )
        
        authenticated_user = await user_service.authenticate_user(login_request)
        assert authenticated_user is not None
        assert authenticated_user.id == created_user.id
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_async_batch_operations(self, async_db_session: AsyncSession) -> None:
        """Test batch operations with async database."""
        user_service = UserService(async_db_session)
        
        # Create multiple users in batch
        user_data_list = [
            {
                "email": f"batch{i}@example.com",
                "password": "TestPassword123!",
                "full_name": f"Batch User {i}"
            }
            for i in range(5)
        ]
        
        created_users = []
        for user_data in user_data_list:
            from app.schemas.auth import UserRegisterRequest
            register_request = UserRegisterRequest(**user_data)
            user = await user_service.create_user(register_request)
            created_users.append(user)
        
        # Verify all users were created
        assert len(created_users) == 5
        
        # Verify all users can be retrieved
        for i, user in enumerate(created_users):
            retrieved_user = await user_service.get_user_by_email(f"batch{i}@example.com")
            assert retrieved_user is not None
            assert retrieved_user.id == user.id


class TestAsyncCacheIntegration:
    """Test async caching integration."""
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_user_caching_async(self, async_db_session: AsyncSession, async_redis_mock) -> None:
        """Test async user caching operations."""
        user_service = UserService(async_db_session)
        
        # Create user
        user_data = {
            "email": "cached@example.com",
            "password": "TestPassword123!",
            "full_name": "Cached User"
        }
        
        from app.schemas.auth import UserRegisterRequest
        register_request = UserRegisterRequest(**user_data)
        
        user = await user_service.create_user(register_request)
        
        # Simulate caching user data
        import json
        user_cache_key = f"user:{user.email}"
        user_data_json = json.dumps({
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active
        })
        
        await async_redis_mock.setex(user_cache_key, 3600, user_data_json)
        
        # Verify cached data
        cached_data = await async_redis_mock.get(user_cache_key)
        assert cached_data is not None
        
        cached_user_data = json.loads(cached_data)
        assert cached_user_data["email"] == user.email
        assert cached_user_data["full_name"] == user.full_name
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_session_management_async(self, async_redis_mock) -> None:
        """Test async session management operations."""
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        session_token = "session.token.here"
        
        # Store session
        session_key = f"session:{session_token}"
        await async_redis_mock.setex(session_key, 1800, user_id)  # 30 minutes
        
        # Retrieve session
        stored_user_id = await async_redis_mock.get(session_key)
        assert stored_user_id == user_id
        
        # Delete session (logout)
        await async_redis_mock.delete(session_key)
        
        # Verify session is deleted
        deleted_session = await async_redis_mock.get(session_key)
        assert deleted_session is None