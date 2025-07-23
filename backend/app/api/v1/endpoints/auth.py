"""
Authentication endpoints for user login, registration, and token management.

Handles user authentication, registration, password reset, and email verification.
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    verify_token,
    generate_password_reset_token,
    verify_password_reset_token,
    generate_email_verification_token,
    verify_email_verification_token,
)
from app.models import User
from app.schemas import (
    UserCreate,
    UserLogin,
    UserLoginResponse,
    UserResponse,
    TokenRefresh,
    TokenResponse,
    PasswordResetRequest,
    PasswordReset,
    EmailVerificationRequest,
    EmailVerification,
    MessageResponse,
)
from app.utils.deps import get_db, get_current_user
from app.utils.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ValidationError,
    ERROR_RESPONSES,
)


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: ERROR_RESPONSES[409],
        422: ERROR_RESPONSES[422],
    },
    summary="Register new user",
    description="Create a new user account with email verification required.",
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Created user data
        
    Raises:
        ConflictError: If username or email already exists
        ValidationError: If input data is invalid
    """
    # Check if username already exists
    username_result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if username_result.scalar_one_or_none():
        raise ConflictError(
            message="Username already registered",
            details={"field": "username", "value": user_data.username}
        )
    
    # Check if email already exists
    email_result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if email_result.scalar_one_or_none():
        raise ConflictError(
            message="Email already registered",
            details={"field": "email", "value": user_data.email}
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        bio=user_data.bio,
        is_active=True,
        is_verified=not settings.ENABLE_EMAIL_VERIFICATION,  # Auto-verify if email verification disabled
    )
    
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


@router.post(
    "/login",
    response_model=UserLoginResponse,
    responses={
        401: ERROR_RESPONSES[401],
        422: ERROR_RESPONSES[422],
    },
    summary="User login",
    description="Authenticate user and return access and refresh tokens.",
)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Authenticate user and return tokens.
    
    Args:
        login_data: Login credentials
        db: Database session
        
    Returns:
        Access token, refresh token, and user data
        
    Raises:
        AuthenticationError: If credentials are invalid
    """
    # Find user by username or email
    user_result = await db.execute(
        select(User).where(
            (User.username == login_data.username) | 
            (User.email == login_data.username)
        )
    )
    user = user_result.scalar_one_or_none()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise AuthenticationError("Invalid username or password")
    
    if not user.is_active:
        raise AuthenticationError("Account is inactive")
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    if login_data.remember_me:
        # Extend token expiration for "remember me"
        access_token_expires = timedelta(days=7)
        refresh_token_expires = timedelta(days=30)
    
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        subject=user.id, expires_delta=refresh_token_expires
    )
    
    # Update last login
    user.last_login = db.bind.dialect.name == 'postgresql' and db.execute(select(db.bind.dialect.current_timestamp)) or None
    await db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
        "user": user,
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
    responses={
        401: ERROR_RESPONSES[401],
        422: ERROR_RESPONSES[422],
    },
    summary="Refresh access token",
    description="Get a new access token using a valid refresh token.",
)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Refresh access token using refresh token.
    
    Args:
        token_data: Refresh token data
        db: Database session
        
    Returns:
        New access token
        
    Raises:
        AuthenticationError: If refresh token is invalid
    """
    user_id = verify_token(token_data.refresh_token, token_type="refresh")
    if not user_id:
        raise AuthenticationError("Invalid refresh token")
    
    # Verify user still exists and is active
    user = await db.get(User, int(user_id))
    if not user or not user.is_active:
        raise AuthenticationError("User not found or inactive")
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds()),
    }


@router.post(
    "/password-reset-request",
    response_model=MessageResponse,
    responses={
        404: ERROR_RESPONSES[404],
        422: ERROR_RESPONSES[422],
    },
    summary="Request password reset",
    description="Send password reset email to user.",
)
async def request_password_reset(
    reset_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Request password reset.
    
    Args:
        reset_data: Password reset request data
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        NotFoundError: If email not found
    """
    # Find user by email
    user_result = await db.execute(
        select(User).where(User.email == reset_data.email)
    )
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError("Email address not found")
    
    if not user.is_active:
        raise AuthenticationError("Account is inactive")
    
    # Generate password reset token
    reset_token = generate_password_reset_token(user.email)
    
    # TODO: Send email with reset token
    # For now, we'll just return success
    # In production, integrate with email service
    
    return {"message": "Password reset email sent"}


@router.post(
    "/password-reset",
    response_model=MessageResponse,
    responses={
        400: ERROR_RESPONSES[400],
        404: ERROR_RESPONSES[404],
        422: ERROR_RESPONSES[422],
    },
    summary="Reset password",
    description="Reset user password using reset token.",
)
async def reset_password(
    reset_data: PasswordReset,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Reset user password.
    
    Args:
        reset_data: Password reset data
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        ValidationError: If token is invalid
        NotFoundError: If user not found
    """
    # Verify reset token
    email = verify_password_reset_token(reset_data.token)
    if not email:
        raise ValidationError("Invalid or expired reset token")
    
    # Find user by email
    user_result = await db.execute(
        select(User).where(User.email == email)
    )
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError("User not found")
    
    # Update password
    user.hashed_password = get_password_hash(reset_data.new_password)
    await db.commit()
    
    return {"message": "Password reset successful"}


@router.post(
    "/email-verification-request",
    response_model=MessageResponse,
    responses={
        404: ERROR_RESPONSES[404],
        422: ERROR_RESPONSES[422],
    },
    summary="Request email verification",
    description="Send email verification link to user.",
)
async def request_email_verification(
    verification_data: EmailVerificationRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Request email verification.
    
    Args:
        verification_data: Email verification request data
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        NotFoundError: If email not found
    """
    # Find user by email
    user_result = await db.execute(
        select(User).where(User.email == verification_data.email)
    )
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError("Email address not found")
    
    if user.is_verified:
        return {"message": "Email already verified"}
    
    # Generate verification token
    verification_token = generate_email_verification_token(user.email)
    
    # TODO: Send verification email
    # For now, we'll just return success
    # In production, integrate with email service
    
    return {"message": "Verification email sent"}


@router.post(
    "/email-verification",
    response_model=MessageResponse,
    responses={
        400: ERROR_RESPONSES[400],
        404: ERROR_RESPONSES[404],
        422: ERROR_RESPONSES[422],
    },
    summary="Verify email",
    description="Verify user email using verification token.",
)
async def verify_email(
    verification_data: EmailVerification,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Verify user email.
    
    Args:
        verification_data: Email verification data
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        ValidationError: If token is invalid
        NotFoundError: If user not found
    """
    # Verify token
    email = verify_email_verification_token(verification_data.token)
    if not email:
        raise ValidationError("Invalid or expired verification token")
    
    # Find user by email
    user_result = await db.execute(
        select(User).where(User.email == email)
    )
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError("User not found")
    
    # Update verification status
    user.is_verified = True
    await db.commit()
    
    return {"message": "Email verified successfully"}


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        401: ERROR_RESPONSES[401],
    },
    summary="Get current user",
    description="Get current authenticated user information.",
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user data
    """
    return current_user


@router.post(
    "/logout",
    response_model=MessageResponse,
    responses={
        401: ERROR_RESPONSES[401],
    },
    summary="User logout",
    description="Logout current user (client should discard tokens).",
)
async def logout(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Logout user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    # In a more sophisticated implementation, you might:
    # - Add tokens to a blacklist
    # - Log the logout event
    # - Clear server-side sessions
    
    return {"message": "Logged out successfully"}