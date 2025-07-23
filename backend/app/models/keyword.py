from typing import Optional

from sqlalchemy import ForeignKey, String, Text, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, TimestampMixin


class Category(Base, IDMixin, TimestampMixin):
    """Category model for organizing keywords."""
    
    __tablename__ = "categories"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)  # Hex color code
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relationships
    keywords = relationship("Keyword", back_populates="category")
    
    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"


class Keyword(Base, IDMixin, TimestampMixin):
    """Keyword model for paper classification and filtering."""
    
    __tablename__ = "keywords"
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)
    
    # Keyword information
    keyword: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    aliases: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of alternative terms
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Configuration
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1=low, 2=medium, 3=high
    auto_collect: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Statistics
    papers_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="keywords")
    category = relationship("Category", back_populates="keywords")
    user_papers = relationship("UserPaper", back_populates="keyword")
    
    def __repr__(self) -> str:
        return f"<Keyword(id={self.id}, keyword='{self.keyword}', user_id={self.user_id})>"