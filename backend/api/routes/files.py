"""
File management API routes
"""

import os
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from app.models import (
    FileInfo, ProcessingStatus, FileType, FileUploadResponse,
    FileProcessResponse, ProcessingOptions, APIError
)
from app.dependencies import validate_content_type, validate_file_size, get_current_user
from utils.file_utils import (
    generate_file_id, calculate_file_hash, save_uploaded_file,
    get_file_type_from_content, delete_file, get_storage_path,
    is_supported_file
)
from utils.exceptions import (
    UnsupportedFileTypeError, FileSizeExceededError,
    CorruptedFileError, create_http_exception
)
from utils.logger import get_process_logger, log_file_operation

logger = logging.getLogger(__name__)
process_logger = get_process_logger(__name__)
router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse, tags=["Files"])
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    _: UploadFile = Depends(validate_file_size)
):
    """
    Upload a file for processing

    Supports PDF, Excel (xlsx, xls), and CSV files.
    Maximum file size: 50MB.
    """
    process_id = process_logger.start_process(
        "file_upload",
        filename=file.filename,
        content_type=file.content_type,
        user_id=current_user.get("id") if current_user else None
    )
    
    try:
        process_logger.log_step("validating_file", filename=file.filename)
        
        # Validate file
        if not file.filename:
            raise create_http_exception(
                400, "No filename provided", "NO_FILENAME"
            )

        if not is_supported_file(file.filename, file.content_type):
            process_logger.log_warning(
                f"Unsupported file type: {file.content_type}",
                filename=file.filename,
                content_type=file.content_type
            )
            raise create_http_exception(
                400,
                f"Unsupported file type: {file.content_type}",
                "UNSUPPORTED_FILE_TYPE"
            )

        process_logger.log_step("reading_file_content")
        
        # Read file content
        file_content = await file.read()
        if not file_content:
            raise create_http_exception(
                400, "File is empty", "EMPTY_FILE"
            )

        process_logger.log_step(
            "generating_metadata",
            file_size=len(file_content),
            content_length=len(file_content)
        )
        
        # Generate file metadata
        file_id = generate_file_id()
        file_hash = calculate_file_hash(file_content)
        file_type_enum = FileType(get_file_type_from_content(file.content_type, file.filename))

        process_logger.log_step("saving_file", file_id=file_id)
        
        # Save file to storage
        file_path = await save_uploaded_file(file_content, file_id, file.filename)

        process_logger.log_step("creating_file_info")
        
        # Create file info
        file_info = FileInfo(
            file_id=file_id,
            original_name=file.filename,
            file_type=file_type_enum,
            size=len(file_content),
            upload_time=datetime.now(),
            processing_status=ProcessingStatus.UPLOADED,
            md5_hash=file_hash
        )

        log_file_operation(
            "upload",
            file_id,
            file.filename,
            file_size=len(file_content),
            file_type=file_type_enum.value,
            hash=file_hash
        )

        process_logger.end_process(
            process_id,
            file_id=file_id,
            final_status="uploaded"
        )

        return FileUploadResponse(success=True, data=file_info)

    except UnsupportedFileTypeError as e:
        process_logger.log_error(e, step="file_type_validation")
        raise create_http_exception(400, str(e), "UNSUPPORTED_FILE_TYPE")

    except FileSizeExceededError as e:
        process_logger.log_error(e, step="file_size_validation")
        raise create_http_exception(413, str(e), "FILE_TOO_LARGE")

    except Exception as e:
        process_logger.log_error(e)
        raise create_http_exception(
            500, "File upload failed", "UPLOAD_FAILED", {"error": str(e)}
        )


@router.post("/{file_id}/process", response_model=FileProcessResponse, tags=["Files"])
async def process_file(
    file_id: str,
    processing_options: ProcessingOptions = ProcessingOptions(),
    current_user: dict = Depends(get_current_user)
):
    """
    Process uploaded file to Markdown format

    Converts PDF, Excel, or CSV files to structured Markdown content
    with table extraction and data parsing.
    """
    process_id = process_logger.start_process(
        "file_processing",
        file_id=file_id,
        processing_options=processing_options.dict(),
        user_id=current_user.get("id") if current_user else None
    )
    
    try:
        process_logger.log_step("validating_file_id", file_id=file_id)
        
        from app.config import get_settings
        settings = get_settings()

        process_logger.log_step("loading_file_data")
        
        # Get actual file path from storage
        import os
        import glob
        storage_path = settings.upload_dir
        
        # Find file by ID
        matching_files = glob.glob(os.path.join(storage_path, f"{file_id}_*"))
        if not matching_files:
            raise create_http_exception(
                404, "File not found", "FILE_NOT_FOUND"
            )
        
        file_path = matching_files[0]
        original_filename = os.path.basename(file_path).replace(f"{file_id}_", "")
        
        process_logger.log_step("detecting_file_type", filename=original_filename)
        
        # Import processors
        from processors.csv_processor import CSVProcessor
        from processors.excel_processor import ExcelProcessor  
        from processors.pdf_processor import PDFProcessor
        
        # Determine file type and processor
        file_ext = original_filename.lower().split('.')[-1]
        processor = None
        file_type_enum = None
        
        if file_ext == 'csv':
            processor = CSVProcessor()
            file_type_enum = FileType.CSV
        elif file_ext in ['xlsx', 'xls']:
            processor = ExcelProcessor()
            file_type_enum = FileType.EXCEL
        elif file_ext == 'pdf':
            processor = PDFProcessor()
            file_type_enum = FileType.PDF
        else:
            raise create_http_exception(
                400, f"Unsupported file type: {file_ext}", "UNSUPPORTED_FILE_TYPE"
            )
        
        process_logger.log_step("processing_file_content", processor=type(processor).__name__)
        
        # Process the file
        processing_result = await processor.process(file_path, processing_options.dict())
        
        process_logger.log_step("processing_completed", 
                              tables_extracted=len(processing_result.get('structured_data', [])))
        
        # Create updated file info
        file_info = FileInfo(
            file_id=file_id,
            original_name=original_filename,
            file_type=file_type_enum,
            size=os.path.getsize(file_path),
            upload_time=datetime.now(),
            processing_status=ProcessingStatus.COMPLETED,
            md5_hash="",  # Would calculate if needed
            processed_content=processing_result.get('markdown_content', ''),
            structured_data=processing_result.get('structured_data', []),
            tables_extracted=len(processing_result.get('structured_data', [])),
            has_structured_data=len(processing_result.get('structured_data', [])) > 0,
            extracted_at=datetime.now(),
            processing_time=processing_result.get('metadata', {}).get('processing_time', 0)
        )

        actual_processing_time = processing_result.get('metadata', {}).get('processing_time', 0)
        actual_tables_extracted = len(processing_result.get('structured_data', []))

        process_logger.log_step(
            "processing_completed",
            processing_time=actual_processing_time,
            tables_extracted=actual_tables_extracted,
            has_structured_data=actual_tables_extracted > 0
        )

        log_file_operation(
            "process",
            file_id,
            file_info.original_name,
            processing_time=actual_processing_time,
            tables_extracted=actual_tables_extracted,
            final_status="completed"
        )

        process_logger.end_process(
            process_id,
            file_id=file_id,
            processing_time=actual_processing_time,
            tables_extracted=actual_tables_extracted
        )

        return FileProcessResponse(success=True, data=file_info)

    except Exception as e:
        process_logger.log_error(e, file_id=file_id)
        log_file_operation(
            "process_failed",
            file_id,
            error=str(e)
        )
        raise create_http_exception(
            500, "File processing failed", "PROCESSING_FAILED", {"error": str(e)}
        )


@router.get("/{file_id}", tags=["Files"])
async def get_file_info(
    file_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get file information and processing status
    """
    try:
        # Placeholder implementation
        # In real implementation, get file info from storage/database

        file_info = FileInfo(
            file_id=file_id,
            original_name="sample_file.pdf",
            file_type=FileType.PDF,
            size=1024000,
            upload_time=datetime.now(),
            processing_status=ProcessingStatus.COMPLETED,
            has_structured_data=True,
            tables_extracted=1
        )

        return {"success": True, "data": file_info.dict()}

    except Exception as e:
        logger.error(f"Failed to get file info for {file_id}: {e}", exc_info=True)
        raise create_http_exception(
            404, "File not found", "FILE_NOT_FOUND", {"file_id": file_id}
        )


@router.delete("/{file_id}", tags=["Files"])
async def delete_file(
    file_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete uploaded file and associated data
    """
    try:
        # Placeholder implementation
        # In real implementation, delete from storage/database

        # Try to delete file from uploads directory
        upload_dir = get_storage_path("uploads")
        for filename in os.listdir(upload_dir):
            if filename.startswith(file_id):
                file_path = os.path.join(upload_dir, filename)
                if delete_file(file_path):
                    logger.info(f"File deleted: {file_path}")

        return {"success": True, "message": "File and associated data deleted successfully"}

    except Exception as e:
        logger.error(f"Failed to delete file {file_id}: {e}", exc_info=True)
        raise create_http_exception(
            500, "File deletion failed", "DELETE_FAILED", {"error": str(e)}
        )


@router.get("/supported-formats", tags=["Files"])
async def get_supported_formats():
    """
    Get list of supported file formats and their capabilities
    """
    try:
        supported_formats = {
            "input_formats": [
                {
                    "format": "pdf",
                    "mime_types": ["application/pdf"],
                    "extensions": [".pdf"],
                    "max_size_mb": 50,
                    "features": ["table_extraction", "text_extraction", "ocr_support"]
                },
                {
                    "format": "excel",
                    "mime_types": [
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        "application/vnd.ms-excel"
                    ],
                    "extensions": [".xlsx", ".xls"],
                    "max_size_mb": 50,
                    "features": ["multi_sheet", "formula_support", "formatting_preservation"]
                },
                {
                    "format": "csv",
                    "mime_types": ["text/csv", "application/csv"],
                    "extensions": [".csv"],
                    "max_size_mb": 50,
                    "features": ["delimiter_detection", "encoding_detection"]
                }
            ],
            "output_formats": [
                {
                    "format": "excel",
                    "extensions": [".xlsx"],
                    "features": ["highlighting", "charts", "formatting"]
                },
                {
                    "format": "pdf",
                    "extensions": [".pdf"],
                    "features": ["formatting", "bookmarking", "compression"]
                },
                {
                    "format": "html",
                    "extensions": [".html"],
                    "features": ["interactive", "responsive", "printable"]
                }
            ]
        }

        return {"success": True, "data": supported_formats}

    except Exception as e:
        logger.error(f"Failed to get supported formats: {e}", exc_info=True)
        raise create_http_exception(
            500, "Failed to get supported formats", "FORMATS_ERROR"
        )


@router.post("/validate-file", tags=["Files"])
async def validate_file(
    file_name: str,
    file_size: int,
    file_type: str,
    checksum: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Validate file before upload
    """
    try:
        # Check file type
        valid_extensions = {"pdf", "xlsx", "xls", "csv"}
        extension = file_name.lower().split('.')[-1] if '.' in file_name else ""

        if extension not in valid_extensions:
            return {
                "valid": False,
                "validation_details": {
                    "file_type_supported": False,
                    "size_within_limits": True,
                    "format_valid": False
                },
                "errors": [f"Unsupported file type: {extension}"],
                "warnings": []
            }

        # Check file size
        max_size_bytes = 50 * 1024 * 1024  # 50MB
        size_valid = file_size <= max_size_bytes

        # Additional validation could be added here

        return {
            "valid": True,
            "validation_details": {
                "file_type_supported": True,
                "size_within_limits": size_valid,
                "format_valid": True,
                "estimated_processing_time": min(file_size / (1024 * 1024), 30)  # Max 30 seconds
            },
            "warnings": [] if size_valid else ["File size is large, processing may take longer"],
            "errors": [] if size_valid else ["File size exceeds maximum allowed limit"]
        }

    except Exception as e:
        logger.error(f"File validation failed: {e}", exc_info=True)
        raise create_http_exception(
            500, "File validation failed", "VALIDATION_FAILED", {"error": str(e)}
        )