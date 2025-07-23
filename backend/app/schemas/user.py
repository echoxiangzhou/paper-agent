"""
Pydantic schemas for user-related operations.

Defines request/response models for user authentication, registration, and management.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    bio: Optional[str] = Field(None, max_length=1000, description="User biography")
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate username format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, hyphens, and underscores")
        return v.lower()


class UserCreate(UserBase):
    """Schema for user registration."""
    
    password: str = Field(..., min_length=8, max_length=100, description="Password")
    confirm_password: str = Field(..., description="Password confirmation")
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        
        return v
    
    def model_post_init(self, __context) -> None:
        """Validate that passwords match."""
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")


class UserUpdate(BaseModel):
    """Schema for user profile updates."""
    
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=1000)


class UserPasswordUpdate(BaseModel):
    """Schema for password updates."""
    
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    confirm_password: str = Field(..., description="New password confirmation")
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        
        return v
    
    def model_post_init(self, __context) -> None:
        """Validate that passwords match."""
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")


class UserResponse(UserBase):
    """Schema for user response data."""
    
    id: int
    is_active: bool
    is_verified: bool
    is_superuser: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")
    remember_me: bool = Field(False, description="Remember me for longer session")


class UserLoginResponse(BaseModel):
    """Schema for login response."""
    
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserResponse = Field(..., description="User information")


class TokenRefresh(BaseModel):
    """Schema for token refresh."""
    
    refresh_token: str = Field(..., description="Refresh token")


class TokenResponse(BaseModel):
    """Schema for token response."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    
    email: EmailStr = Field(..., description="Email address")


class PasswordReset(BaseModel):
    """Schema for password reset."""
    
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    confirm_password: str = Field(..., description="New password confirmation")
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        
        return v
    
    def model_post_init(self, __context) -> None:
        """Validate that passwords match."""
        if self.new_password != self.confirm_password:
            raise ValueError("Passwords do not match")


class EmailVerificationRequest(BaseModel):
    """Schema for email verification request."""
    
    email: EmailStr = Field(..., description="Email address")


class EmailVerification(BaseModel):
    """Schema for email verification."""
    
    token: str = Field(..., description="Email verification token")


class APIKeyCreate(BaseModel):
    """Schema for API key creation."""
    
    name: str = Field(..., min_length=1, max_length=100, description="API key name")
    description: Optional[str] = Field(None, max_length=500, description="API key description")


class APIKeyResponse(BaseModel):
    """Schema for API key response."""
    
    name: str
    api_key: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for paginated user list response."""
    
    users: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int


class MessageResponse(BaseModel):
    """Schema for simple message responses."""
    
    message: str = Field(..., description="Response message")