"""
File handling utilities
"""

import os
import hashlib
import uuid
import aiofiles
import logging
from typing import Optional, BinaryIO
from pathlib import Path

from app.config import get_settings
from .exceptions import FileSizeExceededError, CorruptedFileError

logger = logging.getLogger(__name__)
settings = get_settings()


def generate_file_id() -> str:
    """Generate unique file ID"""
    return str(uuid.uuid4())


def calculate_file_hash(file_content: bytes) -> str:
    """Calculate MD5 hash of file content"""
    return hashlib.md5(file_content).hexdigest()


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return Path(filename).suffix.lower().lstrip('.')


def validate_file_size(file_size: int) -> None:
    """Validate file size against maximum allowed size"""
    max_size_bytes = settings.max_file_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise FileSizeExceededError(file_size, max_size_bytes)


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


def get_file_type_from_content(content_type: str, filename: str) -> str:
    """Determine file type from content type and filename"""
    extension = get_file_extension(filename)

    type_mapping = {
        "pdf": "pdf",
        "xlsx": "xlsx",
        "xls": "xls",
        "csv": "csv"
    }

    return type_mapping.get(extension, "unknown")


async def save_uploaded_file(file_content: bytes, file_id: str, original_name: str) -> str:
    """Save uploaded file to storage"""
    try:
        # Create filename with original name and ID
        file_extension = get_file_extension(original_name)
        filename = f"{file_id}_{original_name}"

        # Ensure upload directory exists
        upload_dir = Path(settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Save file
        file_path = upload_dir / filename
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)

        logger.info(f"File saved: {file_path}")
        return str(file_path)

    except Exception as e:
        logger.error(f"Failed to save file {file_id}: {e}")
        raise


async def read_file(file_path: str) -> bytes:
    """Read file content asynchronously"""
    try:
        async with aiofiles.open(file_path, 'rb') as f:
            return await f.read()
    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise CorruptedFileError(f"Cannot read file: {e}")


def delete_file(file_path: str) -> bool:
    """Delete file from storage"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File deleted: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {e}")
        return False


def get_storage_path(file_type: str = "uploads") -> str:
    """Get storage path based on file type"""
    paths = {
        "uploads": settings.upload_dir,
        "processed": settings.processed_dir,
        "exports": settings.export_dir
    }
    return paths.get(file_type, settings.upload_dir)


def ensure_directory_exists(directory: str) -> None:
    """Ensure directory exists"""
    Path(directory).mkdir(parents=True, exist_ok=True)


def cleanup_old_files(directory: str, max_age_hours: int = 24) -> int:
    """Clean up old files in directory"""
    import time

    if not os.path.exists(directory):
        return 0

    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted_count = 0

    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age_seconds:
                    os.remove(file_path)
                    deleted_count += 1
                    logger.info(f"Deleted old file: {file_path}")

    except Exception as e:
        logger.error(f"Error during cleanup of {directory}: {e}")

    return deleted_count


def get_file_info(file_path: str) -> dict:
    """Get file information"""
    try:
        stat = os.stat(file_path)
        return {
            "path": file_path,
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "exists": True
        }
    except Exception:
        return {
            "path": file_path,
            "exists": False
        }


def validate_file_integrity(file_path: str, expected_hash: str = None) -> bool:
    """Validate file integrity"""
    try:
        # Check if file exists and is readable
        if not os.path.exists(file_path) or not os.access(file_path, os.R_OK):
            return False

        # Check file size
        if os.path.getsize(file_path) == 0:
            return False

        # If hash provided, validate it
        if expected_hash:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            actual_hash = calculate_file_hash(file_content)
            return actual_hash == expected_hash

        return True

    except Exception as e:
        logger.error(f"File integrity validation failed for {file_path}: {e}")
        return False