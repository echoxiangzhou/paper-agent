from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, TimestampMixin


class User(Base, IDMixin, TimestampMixin):
    """User model for authentication and user management."""
    
    __tablename__ = "users"
    
    # Basic user information
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # User profile
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # User status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Activity tracking
    last_login: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Relationships
    email_configs = relationship("EmailConfig", back_populates="user", cascade="all, delete-orphan")
    keywords = relationship("Keyword", back_populates="user", cascade="all, delete-orphan")
    user_papers = relationship("UserPaper", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"