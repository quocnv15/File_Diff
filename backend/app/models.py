"""
Pydantic models for the File Comparison Backend
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class ProcessingStatus(str, Enum):
    """File processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DELETED = "deleted"


class FileType(str, Enum):
    """Supported file types"""
    PDF = "pdf"
    EXCEL = "xlsx"
    EXCEL_LEGACY = "xls"
    CSV = "csv"


class DifferenceSeverity(str, Enum):
    """Difference severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ExportFormat(str, Enum):
    """Export formats"""
    EXCEL = "excel"
    PDF = "pdf"
    HTML = "html"
    CSV = "csv"


class ComparisonType(str, Enum):
    """Comparison types"""
    PRODUCTS = "products"
    INVOICES = "invoices"
    CONTRACTS = "contracts"
    CUSTOM = "custom"


# File Models
class FileInfo(BaseModel):
    """File information model"""
    file_id: str
    original_name: str
    file_type: FileType
    size: int
    upload_time: datetime
    processing_status: ProcessingStatus
    md5_hash: Optional[str] = None
    processed_content: Optional[str] = None
    structured_data: Optional[List[Dict[str, Any]]] = None
    processing_time: Optional[float] = None
    extracted_at: Optional[datetime] = None
    tables_extracted: Optional[int] = None
    has_structured_data: bool = False

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class ProcessingOptions(BaseModel):
    """File processing options"""
    extract_tables: bool = True
    extract_text: bool = True
    preserve_formatting: bool = True
    ocr_enabled: bool = False
    target_language: str = "vi"

    model_config = {"extra": "allow"}


# Comparison Models
class ToleranceSettings(BaseModel):
    """Tolerance settings for numerical comparison"""
    quantity: float = 0.1  # 10%
    unit_price: float = 0.01  # 1%
    amount: float = 0.01  # 1%

    model_config = {"extra": "allow"}


class ComparisonOptions(BaseModel):
    """Comparison configuration options"""
    comparison_type: ComparisonType = ComparisonType.PRODUCTS
    exact_match: bool = True
    ignore_formatting: bool = True
    check_totals: bool = True
    tolerance_settings: ToleranceSettings = ToleranceSettings()
    field_mapping: Optional[Dict[str, List[str]]] = None

    model_config = {"extra": "allow"}


class ComparisonSummary(BaseModel):
    """Comparison summary statistics"""
    total_rows_compared: int
    matching_rows: int
    different_rows: int
    missing_rows: int
    accuracy_rate: float
    total_differences: int
    comparison_time: float

    def round_accuracy_rate(self):
        return round(self.accuracy_rate, 2)


class DifferenceDetail(BaseModel):
    """Detailed difference information"""
    row_number: int
    field: str
    value1: Union[str, float, int, None]
    value2: Union[str, float, int, None]
    difference: Optional[float] = None
    percentage_diff: Optional[float] = None
    severity: DifferenceSeverity
    item1: Optional[Dict[str, Any]] = None
    item2: Optional[Dict[str, Any]] = None


class ComparisonResult(BaseModel):
    """Complete comparison result"""
    comparison_id: str
    file1_info: FileInfo
    file2_info: FileInfo
    summary: ComparisonSummary
    detailed_differences: List[DifferenceDetail]
    processed_at: datetime
    status: str = "completed"

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class ComparisonSummaryResponse(BaseModel):
    """Comparison summary response"""
    comparison_id: str
    summary_statistics: ComparisonSummary
    key_differences: List[Dict[str, Any]]
    recommendations: List[str]


# Export Models
class ExportOptions(BaseModel):
    """Export configuration options"""
    include_summary: bool = True
    include_detailed_differences: bool = True
    include_original_data: bool = False
    highlight_differences: bool = True
    template: str = "standard"
    language: str = "vi"

    model_config = {"extra": "allow"}


class FormattingOptions(BaseModel):
    """Export formatting options"""
    font_size: int = 11
    page_orientation: str = "portrait"
    include_charts: bool = True

    model_config = {"extra": "allow"}


class ExportRequest(BaseModel):
    """Export request model"""
    comparison_id: str
    export_format: ExportFormat
    export_options: ExportOptions = ExportOptions()
    formatting_options: Optional[FormattingOptions] = None


class ExportResponse(BaseModel):
    """Export response model"""
    export_id: str
    export_format: ExportFormat
    file_name: str
    file_size: int
    download_url: str
    expires_at: datetime
    generated_at: datetime

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


# API Request/Response Models
class FileUploadResponse(BaseModel):
    """File upload response"""
    success: bool
    data: FileInfo


class FileProcessResponse(BaseModel):
    """File processing response"""
    success: bool
    data: FileInfo


class CompareFilesRequest(BaseModel):
    """Compare files request"""
    file1_id: str
    file2_id: str
    comparison_options: ComparisonOptions = ComparisonOptions()


class CompareFilesResponse(BaseModel):
    """Compare files response"""
    success: bool
    data: ComparisonResult


class ValidationError(BaseModel):
    """Validation error model"""
    field: str
    message: str
    value: Any


class APIError(BaseModel):
    """API error response"""
    success: bool = False
    error: Dict[str, Any]
    timestamp: datetime
    request_id: Optional[str] = None

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str
    uptime: int
    system_info: Dict[str, float]
    dependencies: Dict[str, str]

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class SupportedFormat(BaseModel):
    """Supported file format model"""
    format: str
    mime_types: List[str]
    extensions: List[str]
    max_size_mb: int
    features: List[str]


class SupportedFormatsResponse(BaseModel):
    """Supported formats response"""
    success: bool
    data: Dict[str, List[SupportedFormat]]


class FileValidationRequest(BaseModel):
    """File validation request"""
    file_name: str
    file_size: int
    file_type: str
    checksum: Optional[str] = None


class FileValidationResponse(BaseModel):
    """File validation response"""
    valid: bool
    validation_details: Dict[str, Any]
    warnings: List[str]
    errors: List[str]


# Utility Models
class StatisticsCard(BaseModel):
    """Statistics card model"""
    label: str
    value: Union[int, float, str]
    type: str = "success"  # success, error, warning, info


class TableData(BaseModel):
    """Table data model"""
    headers: List[str]
    rows: List[List[Union[str, int, float]]]
    metadata: Optional[Dict[str, Any]] = None


class TableRow(BaseModel):
    """Table row model"""
    row_number: int
    data: Dict[str, Union[str, int, float, None]]
    status: str  # match, difference, warning
    differences: Optional[List[DifferenceDetail]] = None