"""
Dependency injection utilities for FastAPI.

Provides common dependencies for database sessions, authentication, and other shared resources.
"""

from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.core.security import verify_token, verify_api_key
from app.models import User
from app.utils.exceptions import AuthenticationError, AuthorizationError


security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> int:
    """
    Dependency to get current user ID from JWT token.
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        User ID
        
    Raises:
        AuthenticationError: If token is invalid or missing
    """
    if not credentials:
        raise AuthenticationError("Missing authentication credentials")
    
    token = credentials.credentials
    user_id = verify_token(token, token_type="access")
    
    if user_id is None:
        raise AuthenticationError("Invalid or expired token")
    
    try:
        return int(user_id)
    except ValueError:
        raise AuthenticationError("Invalid token format")


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
) -> User:
    """
    Dependency to get current user from database.
    
    Args:
        db: Database session
        user_id: User ID from token
        
    Returns:
        User object
        
    Raises:
        AuthenticationError: If user not found or inactive
    """
    user = await db.get(User, user_id)
    if not user:
        raise AuthenticationError("User not found")
    
    if not user.is_active:
        raise AuthenticationError("User account is inactive")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get current active user.
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        Active user object
        
    Raises:
        AuthenticationError: If user is not active or verified
    """
    if not current_user.is_active:
        raise AuthenticationError("User account is inactive")
    
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dependency to get current verified user.
    
    Args:
        current_user: Current active user
        
    Returns:
        Verified user object
        
    Raises:
        AuthenticationError: If user is not verified
    """
    if not current_user.is_verified:
        raise AuthenticationError("User email is not verified")
    
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dependency to get current superuser.
    
    Args:
        current_user: Current user
        
    Returns:
        Superuser object
        
    Raises:
        AuthorizationError: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise AuthorizationError("Not enough permissions")
    
    return current_user


async def get_user_from_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get user from API key.
    
    Args:
        credentials: HTTP Authorization credentials
        db: Database session
        
    Returns:
        User object
        
    Raises:
        AuthenticationError: If API key is invalid or user not found
    """
    if not credentials:
        raise AuthenticationError("Missing API key")
    
    api_key = credentials.credentials
    key_info = verify_api_key(api_key)
    
    if not key_info:
        raise AuthenticationError("Invalid API key")
    
    user_id = key_info["user_id"]
    user = await db.get(User, user_id)
    
    if not user:
        raise AuthenticationError("User not found")
    
    if not user.is_active:
        raise AuthenticationError("User account is inactive")
    
    return user


async def get_optional_current_user() -> Optional[int]:
    """
    Dependency to optionally get current user ID.
    
    Returns:
        User ID if authenticated, None otherwise
    """
    # This would need to be implemented with proper optional authentication
    # For now, return None to avoid breaking the app
    return None


class RateLimitDep:
    """Rate limiting dependency."""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.request_counts = {}
    
    async def __call__(self, user_id: Optional[int] = Depends(get_optional_current_user)):
        """
        Rate limit based on user ID or IP.
        
        Args:
            user_id: Optional user ID
            
        Raises:
            HTTPException: If rate limit exceeded
        """
        # For now, just return without implementing actual rate limiting
        # This would need Redis or another cache in production
        return True


# Create rate limit instances
rate_limit_standard = RateLimitDep(requests_per_minute=60)
rate_limit_strict = RateLimitDep(requests_per_minute=30)
rate_limit_relaxed = RateLimitDep(requests_per_minute=120)


def require_feature(feature_name: str):
    """
    Dependency factory to require specific features to be enabled.
    
    Args:
        feature_name: Name of the feature to check
        
    Returns:
        Dependency function
    """
    def check_feature():
        # Check if feature is enabled in settings
        # This would integrate with feature flags in production
        return True
    
    return check_feature


def require_role(required_role: str):
    """
    Dependency factory to require specific user roles.
    
    Args:
        required_role: Required role name
        
    Returns:
        Dependency function
    """
    async def check_role(
        current_user: User = Depends(get_current_verified_user)
    ) -> User:
        # In a more complex system, you'd check user roles here
        # For now, we'll use the superuser flag for admin operations
        if required_role == "admin" and not current_user.is_superuser:
            raise AuthorizationError(f"Role '{required_role}' required")
        
        return current_user
    
    return check_role


# Common role dependencies
require_admin = require_role("admin")
require_user = get_current_verified_user