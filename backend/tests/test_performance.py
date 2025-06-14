"""
Performance tests for authentication operations.
"""
import pytest
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
from fastapi.testclient import TestClient

from tests.factories import PerformanceTestDataFactory, UserDataFactory
from tests.test_utils import AuthTestHelper


class TestAuthenticationPerformance:
    """Test authentication endpoint performance."""
    
    @pytest.mark.performance
    def test_registration_performance(self, client: TestClient) -> None:
        """Test user registration endpoint performance."""
        user_data = UserDataFactory()
        
        start_time = time.time()
        response = client.post("/api/v1/auth/register", json=user_data)
        duration = time.time() - start_time
        
        assert response.status_code == 201
        assert duration < 2.0, f"Registration took {duration:.2f}s, should be < 2.0s"
    
    @pytest.mark.performance
    def test_login_performance(self, client: TestClient) -> None:
        """Test user login endpoint performance."""
        # Register user first
        user_data = UserDataFactory()
        client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        start_time = time.time()
        response = client.post("/api/v1/auth/login", json=login_data)
        duration = time.time() - start_time
        
        assert response.status_code == 200
        assert duration < 1.5, f"Login took {duration:.2f}s, should be < 1.5s"
    
    @pytest.mark.performance
    def test_token_refresh_performance(self, client: TestClient) -> None:
        """Test token refresh endpoint performance."""
        # Register and login user
        user_data = UserDataFactory()
        client.post("/api/v1/auth/register", json=user_data)
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        login_data = login_response.json()
        refresh_token = login_data["tokens"]["refresh_token"]
        
        refresh_data = {"refresh_token": refresh_token}
        
        start_time = time.time()
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        duration = time.time() - start_time
        
        assert response.status_code == 200
        assert duration < 1.0, f"Token refresh took {duration:.2f}s, should be < 1.0s"
    
    @pytest.mark.performance
    def test_profile_retrieval_performance(self, client: TestClient) -> None:
        """Test user profile retrieval performance."""
        # Setup authenticated user
        user_data = UserDataFactory()
        client.post("/api/v1/auth/register", json=user_data)
        
        login_response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        login_data = login_response.json()
        access_token = login_data["tokens"]["access_token"]
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        start_time = time.time()
        response = client.get("/api/v1/auth/me", headers=headers)
        duration = time.time() - start_time
        
        assert response.status_code == 200
        assert duration < 0.5, f"Profile retrieval took {duration:.2f}s, should be < 0.5s"


class TestConcurrentOperations:
    """Test concurrent authentication operations."""
    
    @pytest.mark.performance
    def test_concurrent_registrations(self, client: TestClient) -> None:
        """Test concurrent user registrations."""
        user_data_list = PerformanceTestDataFactory.bulk_user_data(10)
        
        def register_user(user_data: Dict[str, Any]) -> tuple[int, float]:
            start_time = time.time()
            response = client.post("/api/v1/auth/register", json=user_data)
            duration = time.time() - start_time
            return response.status_code, duration
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_user = {
                executor.submit(register_user, user_data): user_data 
                for user_data in user_data_list
            }
            
            results = []
            for future in as_completed(future_to_user):
                status_code, duration = future.result()
                results.append((status_code, duration))
        
        total_duration = time.time() - start_time
        
        # All registrations should succeed
        successful_registrations = sum(1 for status, _ in results if status == 201)
        assert successful_registrations == len(user_data_list)
        
        # Total time should be reasonable for concurrent operations
        assert total_duration < 10.0, f"Concurrent registrations took {total_duration:.2f}s"
        
        # Individual operations should still be fast
        max_individual_duration = max(duration for _, duration in results)
        assert max_individual_duration < 3.0, f"Slowest registration: {max_individual_duration:.2f}s"
    
    @pytest.mark.performance
    def test_concurrent_logins(self, client: TestClient) -> None:
        """Test concurrent user logins."""
        # Pre-register users
        user_data_list = PerformanceTestDataFactory.concurrent_login_data(5)
        for user_data in user_data_list:
            client.post("/api/v1/auth/register", json={
                "email": user_data["email"],
                "password": user_data["password"],
                "full_name": "Test User"
            })
        
        def login_user(login_data: Dict[str, Any]) -> tuple[int, float]:
            start_time = time.time()
            response = client.post("/api/v1/auth/login", json=login_data)
            duration = time.time() - start_time
            return response.status_code, duration
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_login = {
                executor.submit(login_user, login_data): login_data 
                for login_data in user_data_list
            }
            
            results = []
            for future in as_completed(future_to_login):
                status_code, duration = future.result()
                results.append((status_code, duration))
        
        total_duration = time.time() - start_time
        
        # All logins should succeed
        successful_logins = sum(1 for status, _ in results if status == 200)
        assert successful_logins == len(user_data_list)
        
        # Performance should be reasonable
        assert total_duration < 8.0, f"Concurrent logins took {total_duration:.2f}s"


class TestPasswordHashingPerformance:
    """Test password hashing performance."""
    
    @pytest.mark.performance
    def test_password_hashing_speed(self) -> None:
        """Test password hashing operation speed."""
        from app.core.auth import hash_password
        
        password = "TestPassword123!"
        iterations = 10
        
        start_time = time.time()
        for _ in range(iterations):
            hash_password(password)
        duration = time.time() - start_time
        
        avg_duration = duration / iterations
        assert avg_duration < 0.5, f"Average hash time: {avg_duration:.3f}s, should be < 0.5s"
    
    @pytest.mark.performance
    def test_password_verification_speed(self) -> None:
        """Test password verification operation speed."""
        from app.core.auth import hash_password, verify_password
        
        password = "TestPassword123!"
        hashed = hash_password(password)
        iterations = 50
        
        start_time = time.time()
        for _ in range(iterations):
            verify_password(password, hashed)
        duration = time.time() - start_time
        
        avg_duration = duration / iterations
        assert avg_duration < 0.1, f"Average verify time: {avg_duration:.3f}s, should be < 0.1s"


class TestJWTPerformance:
    """Test JWT token operations performance."""
    
    @pytest.mark.performance
    def test_token_creation_speed(self) -> None:
        """Test JWT token creation speed."""
        from app.core.auth import create_access_token, create_refresh_token
        
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        iterations = 100
        
        # Test access token creation
        start_time = time.time()
        for _ in range(iterations):
            create_access_token(data={"sub": user_id})
        access_duration = time.time() - start_time
        
        # Test refresh token creation
        start_time = time.time()
        for _ in range(iterations):
            create_refresh_token(data={"sub": user_id})
        refresh_duration = time.time() - start_time
        
        avg_access = access_duration / iterations
        avg_refresh = refresh_duration / iterations
        
        assert avg_access < 0.01, f"Average access token creation: {avg_access:.4f}s"
        assert avg_refresh < 0.01, f"Average refresh token creation: {avg_refresh:.4f}s"
    
    @pytest.mark.performance
    def test_token_verification_speed(self) -> None:
        """Test JWT token verification speed."""
        from app.core.auth import create_access_token, verify_token
        
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        token = create_access_token(data={"sub": user_id})
        iterations = 200
        
        start_time = time.time()
        for _ in range(iterations):
            verify_token(token, token_type="access")
        duration = time.time() - start_time
        
        avg_duration = duration / iterations
        assert avg_duration < 0.005, f"Average token verify time: {avg_duration:.4f}s"


class TestDatabasePerformance:
    """Test database operation performance."""
    
    @pytest.mark.performance
    def test_user_lookup_performance(self, client: TestClient) -> None:
        """Test user lookup operation performance."""
        # Register multiple users first
        users = []
        for i in range(10):
            user_data = {
                "email": f"perf{i}@example.com",
                "password": "TestPassword123!",
                "full_name": f"Performance User {i}"
            }
            response = client.post("/api/v1/auth/register", json=user_data)
            assert response.status_code == 201
            users.append(user_data)
        
        # Test login performance for multiple users
        total_time = 0
        for user_data in users:
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }
            
            start_time = time.time()
            response = client.post("/api/v1/auth/login", json=login_data)
            duration = time.time() - start_time
            total_time += duration
            
            assert response.status_code == 200
            assert duration < 2.0, f"User lookup took {duration:.2f}s"
        
        avg_lookup_time = total_time / len(users)
        assert avg_lookup_time < 1.0, f"Average lookup time: {avg_lookup_time:.2f}s"


class TestMemoryUsage:
    """Test memory usage patterns during operations."""
    
    @pytest.mark.performance
    def test_bulk_operations_memory(self, client: TestClient) -> None:
        """Test memory usage during bulk operations."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Perform bulk registrations
        user_data_list = PerformanceTestDataFactory.bulk_user_data(50)
        for user_data in user_data_list:
            response = client.post("/api/v1/auth/register", json=user_data)
            # Allow some to fail due to duplicates
            assert response.status_code in [201, 409]
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB for 50 users)
        assert memory_increase < 100, f"Memory increased by {memory_increase:.1f}MB"


class TestScalabilityMetrics:
    """Test scalability-related metrics."""
    
    @pytest.mark.performance
    def test_response_time_consistency(self, client: TestClient) -> None:
        """Test that response times remain consistent under load."""
        user_data = UserDataFactory()
        client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        # Measure response times for multiple requests
        response_times = []
        for _ in range(20):
            start_time = time.time()
            response = client.post("/api/v1/auth/login", json=login_data)
            duration = time.time() - start_time
            response_times.append(duration)
            assert response.status_code == 200
        
        # Calculate statistics
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        # Response times should be consistent
        time_variance = max_time - min_time
        assert avg_time < 2.0, f"Average response time: {avg_time:.2f}s"
        assert time_variance < 1.0, f"Response time variance: {time_variance:.2f}s"
        assert max_time < 3.0, f"Maximum response time: {max_time:.2f}s"
    
    @pytest.mark.performance
    def test_error_rate_under_load(self, client: TestClient) -> None:
        """Test error rate under load conditions."""
        # Generate unique user data for each registration
        successful_requests = 0
        total_requests = 30
        
        for i in range(total_requests):
            user_data = {
                "email": f"load{i}@example.com",
                "password": "TestPassword123!",
                "full_name": f"Load Test User {i}"
            }
            
            response = client.post("/api/v1/auth/register", json=user_data)
            if response.status_code == 201:
                successful_requests += 1
        
        success_rate = successful_requests / total_requests
        assert success_rate > 0.95, f"Success rate: {success_rate:.2%}, should be > 95%"