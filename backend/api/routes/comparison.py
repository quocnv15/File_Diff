"""
Comparison API routes
"""

import logging
import time
from typing import Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse

from app.models import (
    CompareFilesRequest, CompareFilesResponse, ComparisonResult,
    ComparisonSummaryResponse, ComparisonOptions, ComparisonSummary,
    DifferenceDetail, DifferenceSeverity, FileInfo, ProcessingStatus
)
from app.dependencies import get_current_user
from comparators.data_comparator import DataComparator
from comparators.diff_analyzer import DiffAnalyzer
from utils.exceptions import ComparisonFailedError, create_http_exception
from utils.logger import get_process_logger, log_comparison_operation

logger = logging.getLogger(__name__)
process_logger = get_process_logger(__name__)
router = APIRouter()


@router.post("/compare", response_model=CompareFilesResponse, tags=["Comparison"])
async def compare_files(
    request: CompareFilesRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """
    Compare two processed files

    Compares structured data from two files and returns detailed differences.
    Supports various comparison types and tolerance settings.
    """
    process_id = process_logger.start_process(
        "file_comparison",
        file1_id=request.file1_id,
        file2_id=request.file2_id,
        comparison_options=request.comparison_options.dict(),
        user_id=current_user.get("id") if current_user else None
    )
    
    try:
        process_logger.log_step(
            "validating_request",
            file1_id=request.file1_id,
            file2_id=request.file2_id
        )

        # Validate file IDs
        if not request.file1_id or not request.file2_id:
            raise create_http_exception(
                400, "Both file1_id and file2_id are required", "MISSING_FILE_IDS"
            )

        if request.file1_id == request.file2_id:
            raise create_http_exception(
                400, "Files must be different", "SAME_FILE_IDS"
            )

        process_logger.log_step("retrieving_file_data")
        
        # Get file data (this is a placeholder - in real implementation,
        # you would retrieve from storage/database)
        file1_data = await _get_file_data(request.file1_id)
        file2_data = await _get_file_data(request.file2_id)

        if not file1_data or not file2_data:
            process_logger.log_warning(
                "Files not found or not processed",
                file1_data_available=bool(file1_data),
                file2_data_available=bool(file2_data)
            )
            raise create_http_exception(
                404, "One or both files not found or not processed", "FILES_NOT_READY"
            )

        process_logger.log_step(
            "initializing_comparator",
            file1_rows=len(file1_data.get("structured_data", [])),
            file2_rows=len(file2_data.get("structured_data", []))
        )
        
        # Perform comparison
        comparator = DataComparator()
        comparison_result = await comparator.compare(
            file1_data.get("structured_data", []),
            file2_data.get("structured_data", []),
            request.comparison_options.dict()
        )

        process_logger.log_step("creating_comparison_result")
        
        # Create comparison result object
        comparison_id = comparison_result.get("comparison_id")
        # Create summary from comparison result
        summary_data = comparison_result.get("summary", {})
        comparison_options = request.comparison_options
        summary = ComparisonSummary(
            total_rows_compared=summary_data.get("total_rows_compared", 0),
            matching_rows=summary_data.get("matching_rows", 0),
            different_rows=summary_data.get("different_rows", 0),
            missing_rows=summary_data.get("missing_rows", 0),
            accuracy_rate=summary_data.get("accuracy_rate", 0),
            total_differences=summary_data.get("total_differences", 0),
            comparison_time=summary_data.get("comparison_time", 0)
        )

        process_logger.log_step(
            "processing_differences",
            total_differences=len(comparison_result.get("differences", []))
        )
        
        # Convert difference details
        detailed_differences = []
        for diff_data in comparison_result.get("differences", []):
            # Extract actual difference details from the differences array
            for diff_detail in diff_data.get("differences", []):
                detailed_differences.append(DifferenceDetail(
                    row_number=diff_data.get("row_number", 0),
                    field=diff_detail.field if hasattr(diff_detail, 'field') else diff_detail.get("field", ""),
                    value1=diff_detail.value1 if hasattr(diff_detail, 'value1') else diff_detail.get("value1"),
                    value2=diff_detail.value2 if hasattr(diff_detail, 'value2') else diff_detail.get("value2"),
                    difference=diff_detail.difference if hasattr(diff_detail, 'difference') else diff_detail.get("difference"),
                    percentage_diff=diff_detail.percentage_diff if hasattr(diff_detail, 'percentage_diff') else diff_detail.get("percentage_diff"),
                    severity=diff_detail.severity if hasattr(diff_detail, 'severity') else diff_detail.get("severity", DifferenceSeverity.INFO)
                ))

        process_logger.log_step("creating_comparison_data")
        
        comparison_data = ComparisonResult(
            comparison_id=comparison_id,
            file1_info=_create_file_info(request.file1_id, file1_data),
            file2_info=_create_file_info(request.file2_id, file2_data),
            summary=summary.dict(),
            detailed_differences=detailed_differences,
            processed_at=datetime.now()
        )

        process_logger.log_step("scheduling_cleanup")
        
        # Schedule cleanup task for old comparisons (optional)
        background_tasks.add_task(
            cleanup_old_comparison,
            comparison_id,
            24 * 3600  # 24 hours
        )

        log_comparison_operation(
            "compare",
            comparison_id,
            request.file1_id,
            request.file2_id,
            total_rows_compared=summary.total_rows_compared,
            total_differences=summary.total_differences,
            comparison_time=summary.comparison_time
        )

        process_logger.end_process(
            process_id,
            comparison_id=comparison_id,
            total_differences=len(detailed_differences),
            comparison_time=summary.comparison_time
        )

        return CompareFilesResponse(success=True, data=comparison_data)

    except ComparisonFailedError as e:
        process_logger.log_error(e, file1_id=request.file1_id, file2_id=request.file2_id)
        raise create_http_exception(
            500, str(e), "COMPARISON_FAILED"
        )

    except Exception as e:
        process_logger.log_error(e)
        raise create_http_exception(
            500, "An unexpected error occurred during comparison", "UNEXPECTED_ERROR",
            {"details": str(e)}
        )


@router.get("/{comparison_id}", tags=["Comparison"])
async def get_comparison_results(
    comparison_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed comparison results by ID
    """
    try:
        # In real implementation, retrieve from storage/database
        comparison_data = await _get_comparison_data(comparison_id)

        if not comparison_data:
            raise create_http_exception(
                404, "Comparison not found", "COMPARISON_NOT_FOUND",
                {"comparison_id": comparison_id}
            )

        return {"success": True, "data": comparison_data}

    except Exception as e:
        logger.error(f"Failed to get comparison results: {e}", exc_info=True)
        raise create_http_exception(
            500, "Failed to retrieve comparison results", "RETRIEVAL_FAILED",
            {"comparison_id": comparison_id}
        )


@router.get("/{comparison_id}/summary", response_model=ComparisonSummaryResponse, tags=["Comparison"])
async def get_comparison_summary(
    comparison_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get summary statistics and recommendations for a comparison
    """
    try:
        # Get comparison data
        comparison_data = await _get_comparison_data(comparison_id)

        if not comparison_data:
            raise create_http_exception(
                404, "Comparison not found", "COMPARISON_NOT_FOUND",
                {"comparison_id": comparison_id}
            )

        # Create summary
        summary_data = comparison_data.get("summary", {})
        detailed_differences = comparison_data.get("detailed_differences", [])

        # Analyze differences and create recommendations
        analyzer = DiffAnalyzer()
        field_analysis = analyzer.get_field_analysis(detailed_differences)
        recommendations = analyzer.generate_recommendations(detailed_differences)

        # Create key differences list
        key_differences = []
        if detailed_differences:
            # Get top differences by severity and impact
            sorted_diffs = sorted(
                detailed_differences[:10],  # Limit to top 10
                key=lambda d: (
                    d.severity.value in ["critical", "error"],
                    d.percentage_diff or 0
                ),
                reverse=True
            )

            for diff in sorted_diffs:
                key_differences.append({
                    "type": diff.severity.value,
                    "count": 1,
                    "total_impact": diff.difference or 0
                })

        summary_response = ComparisonSummaryResponse(
            comparison_id=comparison_id,
            summary_statistics=summary_data,
            key_differences=key_differences,
            recommendations=recommendations
        )

        return summary_response

    except Exception as e:
        logger.error(f"Failed to get comparison summary: {e}", exc_info=True)
        raise create_http_exception(
            500, "Failed to generate comparison summary", "SUMMARY_FAILED",
            {"comparison_id": comparison_id}
        )


@router.delete("/{comparison_id}", tags=["Comparison"])
async def delete_comparison(
    comparison_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a comparison and associated data
    """
    try:
        # In real implementation, delete from storage/database
        success = await _delete_comparison_data(comparison_id)

        if not success:
            raise create_http_exception(
                404, "Comparison not found", "COMPARISON_NOT_FOUND",
                {"comparison_id": comparison_id}
            )

        logger.info(f"Comparison deleted: {comparison_id}")

        return {"success": True, "message": "Comparison deleted successfully"}

    except Exception as e:
        logger.error(f"Failed to delete comparison: {e}", exc_info=True)
        raise create_http_exception(
            500, "Failed to delete comparison", "DELETE_FAILED",
            {"comparison_id": comparison_id}
        )


@router.get("/comparison-types", tags=["Comparison"])
async def get_comparison_types():
    """
    Get available comparison types and their configurations
    """
    try:
        comparison_types = [
            {
                "type": "products",
                "name": "Product Comparison",
                "description": "Compare product catalogs and specifications",
                "default_tolerances": {
                    "quantity": 0.1,      # 10%
                    "unit_price": 0.01,   # 1%
                    "amount": 0.01        # 1%
                },
                "recommended_fields": ["description", "quantity", "unit_price", "amount"]
            },
            {
                "type": "invoices",
                "name": "Invoice Comparison",
                "description": "Compare invoice data against source documents",
                "default_tolerances": {
                    "quantity": 0.05,     # 5%
                    "unit_price": 0.005,  # 0.5%
                    "amount": 0.005       # 0.5%
                },
                "recommended_fields": ["invoice_number", "description", "quantity", "unit_price", "amount"]
            },
            {
                "type": "contracts",
                "name": "Contract Comparison",
                "description": "Compare contract terms and conditions",
                "default_tolerances": {
                    "quantity": 0.0,      # Exact match
                    "unit_price": 0.0,   # Exact match
                    "amount": 0.0        # Exact match
                },
                "recommended_fields": ["clause", "term", "value", "description"]
            },
            {
                "type": "custom",
                "name": "Custom Comparison",
                "description": "Custom comparison with user-defined settings",
                "default_tolerances": {
                    "quantity": 0.1,      # 10%
                    "unit_price": 0.01,   # 1%
                    "amount": 0.01        # 1%
                },
                "recommended_fields": []
            }
        ]

        return {"success": True, "data": comparison_types}

    except Exception as e:
        logger.error(f"Failed to get comparison types: {e}", exc_info=True)
        raise create_http_exception(
            500, "Failed to get comparison types", "TYPES_ERROR"
        )


# Helper functions - retrieve actual processed file data
async def _get_file_data(file_id: str) -> Dict[str, Any]:
    """Get file data from storage"""
    try:
        from app.config import get_settings
        import os
        import glob
        import json
        
        settings = get_settings()
        storage_path = settings.upload_dir
        
        # Find file by ID - try multiple possible paths
        possible_paths = [
            storage_path,
            os.path.abspath(storage_path),
            os.path.join(os.getcwd(), storage_path),
            os.path.join(os.getcwd(), storage_path.replace('./', '')),
            "/Volumes/Workspace/1-SideProject/File_Diff/backend/storage/uploads"
        ]
        
        matching_files = []
        for path in possible_paths:
            logger.info(f"Looking for file {file_id} in: {path}")
            matching_files = glob.glob(os.path.join(path, f"{file_id}_*"))
            if matching_files:
                break
        
        logger.info(f"Found {len(matching_files)} matching files for {file_id}")
        
        if not matching_files:
            logger.error(f"File not found: {file_id} in paths: {possible_paths}")
            return None
        
        file_path = matching_files[0]
        
        # Try to find processed data file (could be JSON or we need to re-process)
        processed_file = file_path.replace('.pdf', '_processed.json').replace('.xlsx', '_processed.json').replace('.csv', '_processed.json')
        
        if os.path.exists(processed_file):
            # Load pre-processed data
            with open(processed_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Re-process the file to get current data
            logger.info(f"Re-processing file {file_id} for comparison")
            
            # Determine file type
            file_ext = file_path.lower().split('.')[-1]
            
            if file_ext == 'pdf':
                from processors.pdf_processor import PDFProcessor
                processor = PDFProcessor()
            elif file_ext in ['xlsx', 'xls']:
                from processors.excel_processor import ExcelProcessor
                processor = ExcelProcessor()
            elif file_ext == 'csv':
                from processors.csv_processor import CSVProcessor
                processor = CSVProcessor()
            else:
                logger.error(f"Unsupported file type: {file_ext}")
                return None
            
            # Process the file
            result = await processor.process(file_path)
            
            # Save processed data for future use
            with open(processed_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            
            return result
            
    except Exception as e:
        logger.error(f"Failed to get file data for {file_id}: {e}", exc_info=True)
        return None


def _create_file_info(file_id: str, file_data: Dict[str, Any]) -> FileInfo:
    """Create file info object"""
    return FileInfo(
        file_id=file_id,
        original_name=f"sample_file_{file_id}.xlsx",
        file_type="xlsx",
        size=1024000,
        upload_time=datetime.now(),
        processing_status=ProcessingStatus.COMPLETED,
        has_structured_data=True,
        tables_extracted=len([item for item in file_data.get("structured_data", []) if item.get("type") == "table"])
    )


async def _get_comparison_data(comparison_id: str) -> Dict[str, Any]:
    """Get comparison data from storage (placeholder)"""
    # In real implementation, retrieve from storage/database
    return {
        "comparison_id": comparison_id,
        "summary": {
            "total_rows_compared": 2,
            "matching_rows": 1,
            "different_rows": 1,
            "missing_rows": 0,
            "accuracy_rate": 50.0,
            "total_differences": 1,
            "comparison_time": 1.2
        },
        "detailed_differences": [
            {
                "row_number": 2,
                "field": "unit_price",
                "value1": "50.00",
                "value2": "75.00",
                "difference": 25.0,
                "percentage_diff": 50.0,
                "severity": "error"
            }
        ]
    }


async def _delete_comparison_data(comparison_id: str) -> bool:
    """Delete comparison data from storage (placeholder)"""
    # In real implementation, delete from storage/database
    return True


async def cleanup_old_comparison(comparison_id: str, delay_seconds: int):
    """Background task to clean up old comparison data"""
    import asyncio
    await asyncio.sleep(delay_seconds)

    # In real implementation, delete old comparison data
    logger.info(f"Cleaned up old comparison: {comparison_id}")

    # You could also add logic here to archive old comparisons
    # or move them to cold storage