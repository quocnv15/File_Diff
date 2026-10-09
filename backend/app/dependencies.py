"""
FastAPI dependencies and middleware
"""

from fastapi import Depends, HTTPException, status, UploadFile, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import logging
import time
import uuid

from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """Get current user from JWT token (placeholder for future auth)"""
    # For now, we'll skip authentication
    # In production, implement JWT validation here
    return {"user_id": "anonymous", "permissions": ["read", "write"]}


async def validate_file_size(file: UploadFile = None):
    """Validate file size"""
    if file and file.size:
        max_size_bytes = settings.max_file_size_mb * 1024 * 1024
        if file.size > max_size_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size_mb}MB"
            )
    return file


async def log_requests(request: Request, call_next):
    """Log API requests"""
    start_time = time.time()
    request_id = str(uuid.uuid4())

    # Add request ID to request state for logging
    request.state.request_id = request_id

    logger.info(
        f"Request started",
        extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent")
        }
    )

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(
            f"Request completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time": process_time
            }
        )

        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Request failed",
            extra={
                "request_id": request_id,
                "error": str(e),
                "process_time": process_time
            }
        )
        raise


async def rate_limit_check(request: Request):
    """Simple rate limiting check (placeholder)"""
    # In production, implement proper rate limiting with Redis
    client_ip = request.client.host

    # For now, just log the request
    logger.debug(f"Rate limit check for IP: {client_ip}")

    return True


def get_storage_path(file_type: str = "uploads") -> str:
    """Get storage path based on file type"""
    paths = {
        "uploads": settings.upload_dir,
        "processed": settings.processed_dir,
        "exports": settings.export_dir
    }
    return paths.get(file_type, settings.upload_dir)


async def validate_content_type(file: UploadFile):
    """Validate file content type"""
    allowed_types = {
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "application/vnd.ms-excel": "xls",
        "text/csv": "csv",
        "application/csv": "csv"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}"
        )

    return allowed_types[file.content_type]


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return filename.lower().split('.')[-1] if '.' in filename else ""


def is_supported_file(filename: str, content_type: str) -> bool:
    """Check if file is supported"""
    extension = get_file_extension(filename)

    supported_extensions = {"pdf", "xlsx", "xls", "csv"}
    supported_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
        "text/csv",
        "application/csv"
    }

    return extension in supported_extensions and content_type in supported_types