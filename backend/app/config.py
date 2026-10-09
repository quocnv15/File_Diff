"""
Configuration settings for the File Comparison Backend
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # Application Settings
    app_name: str = "File Comparison Backend"
    app_version: str = "1.0.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS Settings
    allowed_origins: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    # File Storage
    upload_dir: str = "./storage/uploads"
    processed_dir: str = "./storage/processed"
    export_dir: str = "./storage/exports"
    max_file_size_mb: int = 50

    # Processing Settings
    pdf_processor: str = "markitdown"
    enable_ocr: bool = False
    ocr_language: str = "eng"

    # Rate Limiting
    rate_limit_uploads: int = 10
    rate_limit_comparisons: int = 20
    rate_limit_exports: int = 5

    # File Retention (hours)
    file_retention_hours: int = 24
    comparison_retention_hours: int = 24
    export_retention_hours: int = 24

    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"

    # Cache Settings (Redis)
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600  # 1 hour

    # Performance
    workers: int = 4
    max_connections: int = 100
    keepalive_timeout: int = 65
    enable_compression: bool = True
    chunk_size: int = 8192
    max_concurrent_uploads: int = 10
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_file_encoding="utf-8"
    )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings"""
    return settings


def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        settings.upload_dir,
        settings.processed_dir,
        settings.export_dir,
        os.path.dirname(settings.log_file)
    ]

    for directory in directories:
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)