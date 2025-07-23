"""
Custom exception classes and error handlers.

Provides structured error handling for the application with proper HTTP status codes
and error messages.
"""

from typing import Any, Dict, Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class PaperAgentException(Exception):
    """Base exception for Paper Agent application."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class AuthenticationError(PaperAgentException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class AuthorizationError(PaperAgentException):
    """Raised when authorization fails."""
    
    def __init__(self, message: str = "Not authorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class ValidationError(PaperAgentException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class NotFoundError(PaperAgentException):
    """Raised when a resource is not found."""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class ConflictError(PaperAgentException):
    """Raised when there's a conflict with existing data."""
    
    def __init__(self, message: str = "Conflict with existing data", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class RateLimitError(PaperAgentException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details=details
        )


class ExternalServiceError(PaperAgentException):
    """Raised when external service fails."""
    
    def __init__(self, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details
        )


class ConfigurationError(PaperAgentException):
    """Raised when there's a configuration error."""
    
    def __init__(self, message: str = "Configuration error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class EmailError(PaperAgentException):
    """Raised when email operations fail."""
    
    def __init__(self, message: str = "Email operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class AIServiceError(PaperAgentException):
    """Raised when AI service operations fail."""
    
    def __init__(self, message: str = "AI service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class PaperProcessingError(PaperAgentException):
    """Raised when paper processing fails."""
    
    def __init__(self, message: str = "Paper processing failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class DatabaseError(PaperAgentException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str = "Database operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


# Exception handlers
async def paper_agent_exception_handler(request: Request, exc: PaperAgentException) -> JSONResponse:
    """
    Handle custom Paper Agent exceptions.
    
    Args:
        request: FastAPI request object
        exc: Paper Agent exception
        
    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "type": exc.__class__.__name__,
                "details": exc.details,
                "path": str(request.url.path),
                "method": request.method
            }
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI HTTP exceptions.
    
    Args:
        request: FastAPI request object
        exc: HTTP exception
        
    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "type": "HTTPException",
                "details": {},
                "path": str(request.url.path),
                "method": request.method
            }
        }
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle Pydantic validation exceptions.
    
    Args:
        request: FastAPI request object
        exc: Validation exception
        
    Returns:
        JSON response with validation error details
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "message": "Validation error",
                "type": "ValidationError",
                "details": {"validation_errors": str(exc)},
                "path": str(request.url.path),
                "method": request.method
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions.
    
    Args:
        request: FastAPI request object
        exc: General exception
        
    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "type": "InternalServerError",
                "details": {"exception": str(exc)} if hasattr(exc, '__str__') else {},
                "path": str(request.url.path),
                "method": request.method
            }
        }
    )


# Error response models for OpenAPI documentation
ERROR_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "Bad request",
                        "type": "ValidationError",
                        "details": {},
                        "path": "/api/v1/example",
                        "method": "POST"
                    }
                }
            }
        }
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "Authentication failed",
                        "type": "AuthenticationError",
                        "details": {},
                        "path": "/api/v1/example",
                        "method": "GET"
                    }
                }
            }
        }
    },
    403: {
        "description": "Forbidden",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "Not authorized",
                        "type": "AuthorizationError",
                        "details": {},
                        "path": "/api/v1/example",
                        "method": "DELETE"
                    }
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "Resource not found",
                        "type": "NotFoundError",
                        "details": {},
                        "path": "/api/v1/example/123",
                        "method": "GET"
                    }
                }
            }
        }
    },
    409: {
        "description": "Conflict",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "Conflict with existing data",
                        "type": "ConflictError",
                        "details": {},
                        "path": "/api/v1/example",
                        "method": "POST"
                    }
                }
            }
        }
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "Validation failed",
                        "type": "ValidationError",
                        "details": {"field": "This field is required"},
                        "path": "/api/v1/example",
                        "method": "POST"
                    }
                }
            }
        }
    },
    429: {
        "description": "Too Many Requests",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "Rate limit exceeded",
                        "type": "RateLimitError",
                        "details": {"retry_after": 60},
                        "path": "/api/v1/example",
                        "method": "POST"
                    }
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "error": {
                        "message": "Internal server error",
                        "type": "InternalServerError",
                        "details": {},
                        "path": "/api/v1/example",
                        "method": "GET"
                    }
                }
            }
        }
    }
}