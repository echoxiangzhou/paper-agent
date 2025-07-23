from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import (
    String, Text, Integer, Float, Boolean, DateTime, 
    ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, TimestampMixin


class PaperStatus(str, Enum):
    """Status of paper processing."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ReadStatus(str, Enum):
    """User's reading status for a paper."""
    UNREAD = "unread"
    READING = "reading"
    READ = "read"
    SAVED = "saved"
    ARCHIVED = "archived"


class Paper(Base, IDMixin, TimestampMixin):
    """Paper model for storing academic papers information."""
    
    __tablename__ = "papers"
    
    # Paper identification
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    authors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    abstract: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Publication details
    journal: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    publication_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    volume: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    issue: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    pages: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Identifiers
    doi: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, unique=True, index=True)
    arxiv_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=True, index=True)
    pmid: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, unique=True, index=True)
    
    # URLs and links
    pdf_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    web_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Content
    full_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # Processing status
    status: Mapped[PaperStatus] = mapped_column(
        SQLEnum(PaperStatus), 
        default=PaperStatus.PENDING, 
        nullable=False, 
        index=True
    )
    
    # Quality metrics
    citation_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    impact_factor: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    h_index: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Processing metadata
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    processing_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Content hash for deduplication
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, unique=True, index=True)
    
    # Relationships
    user_papers = relationship("UserPaper", back_populates="paper", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Paper(id={self.id}, title='{self.title[:50]}...', status={self.status})>"


class UserPaper(Base, IDMixin, TimestampMixin):
    """Association between users and papers with user-specific metadata."""
    
    __tablename__ = "user_papers"
    
    # Foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    paper_id: Mapped[int] = mapped_column(ForeignKey("papers.id"), nullable=False, index=True)
    keyword_id: Mapped[Optional[int]] = mapped_column(ForeignKey("keywords.id"), nullable=True, index=True)
    
    # User-specific data
    read_status: Mapped[ReadStatus] = mapped_column(
        SQLEnum(ReadStatus), 
        default=ReadStatus.UNREAD, 
        nullable=False, 
        index=True
    )
    
    # User ratings and notes
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1-5 stars
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of user tags
    
    # User activity
    bookmarked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    shared: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    downloaded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Reading progress
    last_read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reading_progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # 0.0-1.0
    
    # Discovery metadata
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # email, manual, api, etc.
    collected_from: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # email subject, RSS feed, etc.
    
    # Relationships
    user = relationship("User", back_populates="user_papers")
    paper = relationship("Paper", back_populates="user_papers")
    keyword = relationship("Keyword", back_populates="user_papers")
    
    def __repr__(self) -> str:
        return f"<UserPaper(user_id={self.user_id}, paper_id={self.paper_id}, status={self.read_status})>"