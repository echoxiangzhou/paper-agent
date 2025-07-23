"""
Security utilities for authentication and authorization.

Provides JWT token management, password hashing, and security-related functions.
"""

from datetime import datetime, timedelta
from typing import Any, Optional, Union

import bcrypt
import jwt
from passlib.context import CryptContext

from .config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: The subject (usually user ID) for the token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        subject: The subject (usually user ID) for the token
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT refresh token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        Subject (user ID) if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        
        # Check token type
        if payload.get("type") != token_type:
            return None
            
        subject: str = payload.get("sub")
        if subject is None:
            return None
            
        return subject
    except jwt.PyJWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate password hash.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def generate_password_reset_token(email: str) -> str:
    """
    Generate a password reset token.
    
    Args:
        email: User email address
        
    Returns:
        Password reset token
    """
    delta = timedelta(hours=1)  # Reset token expires in 1 hour
    now = datetime.utcnow()
    expires = now + delta
    
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "type": "password_reset"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify password reset token and return email.
    
    Args:
        token: Password reset token
        
    Returns:
        Email if token is valid, None otherwise
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        
        # Check token type
        if decoded_token.get("type") != "password_reset":
            return None
            
        return decoded_token.get("sub")
    except jwt.PyJWTError:
        return None


def generate_email_verification_token(email: str) -> str:
    """
    Generate an email verification token.
    
    Args:
        email: User email address
        
    Returns:
        Email verification token
    """
    delta = timedelta(days=7)  # Verification token expires in 7 days
    now = datetime.utcnow()
    expires = now + delta
    
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "type": "email_verification"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_email_verification_token(token: str) -> Optional[str]:
    """
    Verify email verification token and return email.
    
    Args:
        token: Email verification token
        
    Returns:
        Email if token is valid, None otherwise
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        
        # Check token type
        if decoded_token.get("type") != "email_verification":
            return None
            
        return decoded_token.get("sub")
    except jwt.PyJWTError:
        return None


def create_api_key(user_id: int, name: str) -> str:
    """
    Create an API key for a user.
    
    Args:
        user_id: User ID
        name: API key name/description
        
    Returns:
        API key string
    """
    # API keys don't expire by default
    payload = {
        "sub": str(user_id),
        "type": "api_key",
        "name": name,
        "iat": datetime.utcnow().timestamp()
    }
    
    encoded_jwt = jwt.encode(
        payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt


def verify_api_key(api_key: str) -> Optional[dict]:
    """
    Verify API key and return user info.
    
    Args:
        api_key: API key string
        
    Returns:
        Dictionary with user_id and key info if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            api_key, settings.SECRET_KEY, algorithms=["HS256"]
        )
        
        # Check token type
        if payload.get("type") != "api_key":
            return None
            
        user_id = payload.get("sub")
        if user_id is None:
            return None
            
        return {
            "user_id": int(user_id),
            "name": payload.get("name"),
            "issued_at": payload.get("iat")
        }
    except jwt.PyJWTError:
        return None