"""
User management endpoints for profile updates, user administration, and account management.

Handles user profile operations, admin user management, and account settings.
"""

from typing import Any, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.security import get_password_hash, verify_password, create_api_key
from app.models import User
from app.schemas import (
    UserResponse,
    UserUpdate,
    UserPasswordUpdate,
    UserListResponse,
    APIKeyCreate,
    APIKeyResponse,
    MessageResponse,
)
from app.utils.deps import (
    get_db,
    get_current_user,
    get_current_verified_user,
    get_current_superuser,
)
from app.utils.exceptions import (
    AuthenticationError,
    NotFoundError,
    ConflictError,
    ValidationError,
    AuthorizationError,
    ERROR_RESPONSES,
)


router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        401: ERROR_RESPONSES[401],
    },
    summary="Get current user profile",
    description="Get current authenticated user's profile information.",
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user profile.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user data
    """
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    responses={
        401: ERROR_RESPONSES[401],
        422: ERROR_RESPONSES[422],
    },
    summary="Update current user profile",
    description="Update current authenticated user's profile information.",
)
async def update_current_user_profile(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update current user profile.
    
    Args:
        user_update: User update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated user data
    """
    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.put(
    "/me/password",
    response_model=MessageResponse,
    responses={
        401: ERROR_RESPONSES[401],
        422: ERROR_RESPONSES[422],
    },
    summary="Update current user password",
    description="Update current authenticated user's password.",
)
async def update_current_user_password(
    password_update: UserPasswordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update current user password.
    
    Args:
        password_update: Password update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
        
    Raises:
        AuthenticationError: If current password is incorrect
    """
    # Verify current password
    if not verify_password(password_update.current_password, current_user.hashed_password):
        raise AuthenticationError("Current password is incorrect")
    
    # Update password
    current_user.hashed_password = get_password_hash(password_update.new_password)
    await db.commit()
    
    return {"message": "Password updated successfully"}


@router.delete(
    "/me",
    response_model=MessageResponse,
    responses={
        401: ERROR_RESPONSES[401],
    },
    summary="Delete current user account",
    description="Delete current authenticated user's account (soft delete).",
)
async def delete_current_user_account(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete current user account.
    
    Args:
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    # Soft delete by deactivating account
    current_user.is_active = False
    await db.commit()
    
    return {"message": "Account deactivated successfully"}


@router.post(
    "/me/api-keys",
    response_model=APIKeyResponse,
    responses={
        401: ERROR_RESPONSES[401],
        422: ERROR_RESPONSES[422],
    },
    summary="Create API key",
    description="Create a new API key for the current user.",
)
async def create_user_api_key(
    api_key_data: APIKeyCreate,
    current_user: User = Depends(get_current_verified_user),
) -> Any:
    """
    Create API key for current user.
    
    Args:
        api_key_data: API key creation data
        current_user: Current authenticated user
        
    Returns:
        Created API key
    """
    # Create API key
    api_key = create_api_key(current_user.id, api_key_data.name)
    
    return {
        "name": api_key_data.name,
        "api_key": api_key,
        "created_at": func.now(),
    }


# Admin endpoints
@router.get(
    "/",
    response_model=UserListResponse,
    responses={
        401: ERROR_RESPONSES[401],
        403: ERROR_RESPONSES[403],
    },
    summary="List users (Admin)",
    description="Get paginated list of users. Requires admin privileges.",
)
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search term for username or email"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
) -> Any:
    """
    List users with pagination and filtering.
    
    Args:
        db: Database session
        current_user: Current authenticated superuser
        page: Page number
        size: Page size
        search: Search term
        is_active: Filter by active status
        is_verified: Filter by verification status
        
    Returns:
        Paginated user list
    """
    # Build query
    query = select(User)
    count_query = select(func.count(User.id))
    
    # Apply filters
    filters = []
    if search:
        search_filter = (
            User.username.ilike(f"%{search}%") |
            User.email.ilike(f"%{search}%") |
            User.full_name.ilike(f"%{search}%")
        )
        filters.append(search_filter)
    
    if is_active is not None:
        filters.append(User.is_active == is_active)
    
    if is_verified is not None:
        filters.append(User.is_verified == is_verified)
    
    if filters:
        query = query.where(and_(*filters))
        count_query = count_query.where(and_(*filters))
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(User.created_at.desc())
    
    # Execute query
    result = await db.execute(query)
    users = result.scalars().all()
    
    # Calculate pages
    pages = (total + size - 1) // size
    
    return {
        "users": users,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        401: ERROR_RESPONSES[401],
        403: ERROR_RESPONSES[403],
        404: ERROR_RESPONSES[404],
    },
    summary="Get user by ID (Admin)",
    description="Get user by ID. Requires admin privileges.",
)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated superuser
        
    Returns:
        User data
        
    Raises:
        NotFoundError: If user not found
    """
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")
    
    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        401: ERROR_RESPONSES[401],
        403: ERROR_RESPONSES[403],
        404: ERROR_RESPONSES[404],
        422: ERROR_RESPONSES[422],
    },
    summary="Update user (Admin)",
    description="Update user by ID. Requires admin privileges.",
)
async def update_user_by_id(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Update user by ID.
    
    Args:
        user_id: User ID
        user_update: User update data
        db: Database session
        current_user: Current authenticated superuser
        
    Returns:
        Updated user data
        
    Raises:
        NotFoundError: If user not found
    """
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")
    
    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user


@router.put(
    "/{user_id}/activate",
    response_model=MessageResponse,
    responses={
        401: ERROR_RESPONSES[401],
        403: ERROR_RESPONSES[403],
        404: ERROR_RESPONSES[404],
    },
    summary="Activate user (Admin)",
    description="Activate user account. Requires admin privileges.",
)
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Activate user account.
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated superuser
        
    Returns:
        Success message
        
    Raises:
        NotFoundError: If user not found
    """
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")
    
    user.is_active = True
    await db.commit()
    
    return {"message": f"User {user.username} activated successfully"}


@router.put(
    "/{user_id}/deactivate",
    response_model=MessageResponse,
    responses={
        401: ERROR_RESPONSES[401],
        403: ERROR_RESPONSES[403],
        404: ERROR_RESPONSES[404],
    },
    summary="Deactivate user (Admin)",
    description="Deactivate user account. Requires admin privileges.",
)
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Deactivate user account.
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated superuser
        
    Returns:
        Success message
        
    Raises:
        NotFoundError: If user not found
        AuthorizationError: If trying to deactivate self
    """
    if user_id == current_user.id:
        raise AuthorizationError("Cannot deactivate your own account")
    
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")
    
    user.is_active = False
    await db.commit()
    
    return {"message": f"User {user.username} deactivated successfully"}


@router.put(
    "/{user_id}/verify",
    response_model=MessageResponse,
    responses={
        401: ERROR_RESPONSES[401],
        403: ERROR_RESPONSES[403],
        404: ERROR_RESPONSES[404],
    },
    summary="Verify user email (Admin)",
    description="Manually verify user email. Requires admin privileges.",
)
async def verify_user_email(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Manually verify user email.
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated superuser
        
    Returns:
        Success message
        
    Raises:
        NotFoundError: If user not found
    """
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")
    
    user.is_verified = True
    await db.commit()
    
    return {"message": f"User {user.username} email verified successfully"}


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    responses={
        401: ERROR_RESPONSES[401],
        403: ERROR_RESPONSES[403],
        404: ERROR_RESPONSES[404],
    },
    summary="Delete user (Admin)",
    description="Permanently delete user account. Requires admin privileges.",
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_superuser),
) -> Any:
    """
    Delete user account permanently.
    
    Args:
        user_id: User ID
        db: Database session
        current_user: Current authenticated superuser
        
    Returns:
        Success message
        
    Raises:
        NotFoundError: If user not found
        AuthorizationError: If trying to delete self
    """
    if user_id == current_user.id:
        raise AuthorizationError("Cannot delete your own account")
    
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")
    
    # In production, you might want to:
    # 1. Check for related data and handle cascading deletes
    # 2. Archive user data before deletion
    # 3. Send notification emails
    
    await db.delete(user)
    await db.commit()
    
    return {"message": f"User {user.username} deleted successfully"}