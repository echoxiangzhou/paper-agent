from typing import Optional
from enum import Enum

from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IDMixin, TimestampMixin


class EmailProvider(str, Enum):
    """Supported email providers."""
    GMAIL = "gmail"
    OUTLOOK = "outlook"
    QQ = "qq"
    NETEASE = "netease"
    IMAP = "imap"  # Generic IMAP


class EmailConfig(Base, IDMixin, TimestampMixin):
    """Email configuration model for connecting to user's email accounts."""
    
    __tablename__ = "email_configs"
    
    # Foreign key
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    
    # Email account details
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Display name for this config
    email_address: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    provider: Mapped[EmailProvider] = mapped_column(SQLEnum(EmailProvider), nullable=False)
    
    # Connection settings
    imap_server: Mapped[str] = mapped_column(String(100), nullable=False)
    imap_port: Mapped[int] = mapped_column(Integer, default=993, nullable=False)
    use_ssl: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Authentication
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # Encrypted
    app_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # For 2FA accounts
    
    # Folder settings
    inbox_folder: Mapped[str] = mapped_column(String(50), default="INBOX", nullable=False)
    processed_folder: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Filtering settings
    search_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    sender_filters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    subject_filters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # Processing settings
    auto_process: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    process_interval: Mapped[int] = mapped_column(Integer, default=300, nullable=False)  # seconds
    max_emails_per_batch: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    
    # Status and monitoring
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_check: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # ISO datetime string
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    connection_status: Mapped[str] = mapped_column(String(20), default="unknown", nullable=False)
    
    # Statistics
    total_processed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    papers_found: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_paper_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Advanced settings
    advanced_settings: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="email_configs")
    
    def __repr__(self) -> str:
        return f"<EmailConfig(id={self.id}, name='{self.name}', email='{self.email_address}', provider={self.provider})>"
    
    @property
    def display_name(self) -> str:
        """Get a display-friendly name for this email config."""
        return f"{self.name} ({self.email_address})"
    
    @property
    def is_healthy(self) -> bool:
        """Check if the email config is in a healthy state."""
        return (
            self.is_active and 
            self.connection_status in ["connected", "idle"] and 
            not self.last_error
        )