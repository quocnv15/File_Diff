"""
Custom exceptions for the File Comparison Backend
"""

from fastapi import HTTPException, status


class FileProcessingError(Exception):
    """Base exception for file processing errors"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class UnsupportedFileTypeError(FileProcessingError):
    """Raised when file type is not supported"""
    def __init__(self, file_type: str):
        super().__init__(
            f"Unsupported file type: {file_type}",
            "UNSUPPORTED_FILE_TYPE"
        )


class FileSizeExceededError(FileProcessingError):
    """Raised when file size exceeds limit"""
    def __init__(self, size: int, max_size: int):
        super().__init__(
            f"File size {size} bytes exceeds maximum allowed size {max_size} bytes",
            "FILE_SIZE_EXCEEDED"
        )


class CorruptedFileError(FileProcessingError):
    """Raised when file is corrupted or invalid"""
    def __init__(self, message: str = "File appears to be corrupted or invalid"):
        super().__init__(message, "CORRUPTED_FILE")


class ProcessingFailedError(FileProcessingError):
    """Raised when file processing fails"""
    def __init__(self, message: str, processing_step: str = None):
        self.processing_step = processing_step
        super().__init__(
            f"Processing failed: {message}",
            "PROCESSING_FAILED"
        )


class ComparisonError(Exception):
    """Base exception for comparison errors"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class InvalidComparisonDataError(ComparisonError):
    """Raised when comparison data is invalid"""
    def __init__(self, message: str = "Invalid comparison data provided"):
        super().__init__(message, "INVALID_COMPARISON_DATA")


class ComparisonFailedError(ComparisonError):
    """Raised when comparison process fails"""
    def __init__(self, message: str):
        super().__init__(f"Comparison failed: {message}", "COMPARISON_FAILED")


class ExportError(Exception):
    """Base exception for export errors"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ExportGenerationError(ExportError):
    """Raised when export generation fails"""
    def __init__(self, message: str, export_format: str = None):
        self.export_format = export_format
        super().__init__(
            f"Export generation failed: {message}",
            "EXPORT_GENERATION_FAILED"
        )


class InvalidExportFormatError(ExportError):
    """Raised when export format is invalid"""
    def __init__(self, format_name: str):
        super().__init__(
            f"Invalid export format: {format_name}",
            "INVALID_EXPORT_FORMAT"
        )


# HTTP Exception helpers
def create_http_exception(status_code: int, message: str, error_code: str = None, details: dict = None):
    """Create HTTPException with standard format"""
    return HTTPException(
        status_code=status_code,
        detail={
            "error": {
                "code": error_code or "HTTP_ERROR",
                "message": message,
                "details": details or {}
            }
        }
    )