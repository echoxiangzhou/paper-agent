"""
Application Configuration

Centralized configuration management using Pydantic Settings.
All settings can be overridden with environment variables.
"""

import secrets
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Basic app info
    PROJECT_NAME: str = "Paper Summary Agent"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # Frontend dev server
        "http://localhost:8080",  # Alternative frontend
        "https://localhost:3000", # HTTPS frontend
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from environment variable."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "paper_agent"
    
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> str:
        """Assemble database URL from components."""
        if isinstance(v, str):
            return v
        values = info.data
        return (
            f"postgresql://{values.get('POSTGRES_USER')}:"
            f"{values.get('POSTGRES_PASSWORD')}@"
            f"{values.get('POSTGRES_SERVER')}:"
            f"{values.get('POSTGRES_PORT', 5432)}/"
            f"{values.get('POSTGRES_DB')}"
        )
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    @property
    def REDIS_URL(self) -> str:
        """Construct Redis URL."""
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Celery
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    @field_validator("CELERY_BROKER_URL", mode="before")
    @classmethod
    def assemble_celery_broker(cls, v: Optional[str], info) -> str:
        """Assemble Celery broker URL."""
        if isinstance(v, str):
            return v
        # Use Redis as broker
        values = info.data
        auth = f":{values.get('REDIS_PASSWORD')}@" if values.get('REDIS_PASSWORD') else ""
        return f"redis://{auth}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/1"
    
    @field_validator("CELERY_RESULT_BACKEND", mode="before")
    @classmethod
    def assemble_celery_result_backend(cls, v: Optional[str], info) -> str:
        """Assemble Celery result backend URL."""
        if isinstance(v, str):
            return v
        # Use Redis as result backend
        values = info.data
        auth = f":{values.get('REDIS_PASSWORD')}@" if values.get('REDIS_PASSWORD') else ""
        return f"redis://{auth}{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}/2"
    
    # AI Services
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DEFAULT_AI_MODEL: str = "google/gemini-flash-1.5"  # Gemini Flash 2.0
    AI_REQUEST_TIMEOUT: int = 60
    AI_MAX_RETRIES: int = 3
    
    # Email Configuration
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = PROJECT_NAME
    
    # Firecrawl
    FIRECRAWL_API_KEY: Optional[str] = None
    FIRECRAWL_BASE_URL: str = "https://api.firecrawl.dev"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # File Storage
    UPLOAD_MAX_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".md"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text
    
    # Features
    ENABLE_BACKGROUND_TASKS: bool = True
    ENABLE_EMAIL_VERIFICATION: bool = True
    ENABLE_PASSWORD_RESET: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()