# File Processing System Documentation

## Overview

The File Comparison system supports multiple file formats with specialized processors for each type. The processing pipeline handles data extraction, normalization, and preparation for comparison operations.

## Supported File Formats

### CSV Files
- **Extensions**: `.csv`
- **Processor**: `CSVProcessor`
- **Encoding**: UTF-8 (auto-detection fallback)
- **Delimiter**: Auto-detect (comma, semicolon, tab)
- **Max Size**: 100MB

### Excel Files
- **Extensions**: `.xlsx`, `.xls`
- **Processor**: `ExcelProcessor`
- **Sheets**: First sheet by default, all sheets optional
- **Cell Types**: Text, numbers, dates, formulas (values only)
- **Max Size**: 100MB

### PDF Files
- **Extensions**: `.pdf`
- **Processor**: `PDFProcessor`
- **Method**: markitdown (primary), PyPDF2 (fallback)
- **Content**: Table extraction and text parsing
- **Max Size**: 50MB

## Processing Pipeline

### Stage 1: File Validation
```python
class FileValidator:
    def validate_file(self, file_path: str) -> ValidationResult:
        # Check file existence and permissions
        # Verify file extension
        # Check file size limits
        # Validate file format integrity
        pass
```

**Validation Checks:**
- File exists and readable
- File extension supported
- File size within limits
- File format not corrupted
- Sufficient disk space for processing

### Stage 2: Data Extraction
```python
class DataExtractor:
    async def extract_data(self, file_path: str) -> ExtractedData:
        # Detect file type
        # Select appropriate processor
        # Extract raw data
        # Handle encoding issues
        pass
```

**Extraction Process:**
1. File type detection from extension and content
2. Processor selection and initialization
3. Raw data extraction with error handling
4. Encoding detection and normalization
5. Basic data structure validation

### Stage 3: Data Normalization
```python
class DataNormalizer:
    def normalize_data(self, raw_data: Any) -> NormalizedData:
        # Standardize data types
        # Handle missing values
        # Normalize text (case, whitespace)
        # Validate data structure
        pass
```

**Normalization Steps:**
- Convert all text to consistent case (configurable)
- Trim whitespace and normalize line endings
- Handle empty/null values consistently
- Standardize numeric formats
- Convert dates to consistent format
- Validate and clean column headers

### Stage 4: Data Structuring
```python
class DataStructurer:
    def structure_data(self, normalized_data: NormalizedData) -> StructuredData:
        # Create standardized DataFrame
        # Add metadata
        # Generate preview
        # Calculate statistics
        pass
```

**Output Structure:**
```python
{
    "metadata": {
        "file_id": "uuid",
        "filename": "example.csv",
        "file_type": "csv",
        "rows": 1000,
        "columns": 5,
        "size_bytes": 10240,
        "processing_time": 0.05
    },
    "data": [
        {"column1": "value1", "column2": "value2"},
        # ... more rows
    ],
    "preview": {
        "first_5_rows": [...],
        "column_types": {"column1": "string", "column2": "number"},
        "null_counts": {"column1": 0, "column2": 2}
    }
}
```

## Processor Implementations

### CSV Processor
```python
class CSVProcessor(FileProcessor):
    def __init__(self):
        self.supported_extensions = ['.csv']
        self.delimiter_options = [',', ';', '\t', '|']
        self.encoding_options = ['utf-8', 'latin-1', 'cp1252']

    async def process_file(self, file_path: str) -> ProcessedData:
        # Auto-detect delimiter
        # Auto-detect encoding
        # Handle quoted fields
        # Parse data with pandas
        return processed_data
```

**Features:**
- Automatic delimiter detection
- Encoding auto-detection with fallback
- Quoted field handling
- Comment line skipping
- Header row detection
- Data type inference

### Excel Processor
```python
class ExcelProcessor(FileProcessor):
    def __init__(self):
        self.supported_extensions = ['.xlsx', '.xls']
        self.engine = 'openpyxl'

    async def process_file(self, file_path: str) -> ProcessedData:
        # Read specified sheet or first sheet
        # Handle merged cells
        # Extract formulas as values
        # Preserve data types
        return processed_data
```

**Features:**
- Multiple sheet support
- Merged cell handling
- Formula evaluation (values only)
- Data type preservation
- Cell formatting detection
- Named range support

### PDF Processor
```python
class PDFProcessor(FileProcessor):
    def __init__(self):
        self.supported_extensions = ['.pdf']
        self.primary_method = 'markitdown'
        self.fallback_method = 'pypdf2'

    async def process_file(self, file_path: str) -> ProcessedData:
        # Try markitdown first
        # Fallback to PyPDF2 if needed
        # Extract tables and text
        # Structure tabular data
        return processed_data
```

**Features:**
- Table extraction from PDF
- Text parsing and structuring
- Multiple page handling
- OCR integration (future)
- Layout analysis

## Configuration Options

### Processing Configuration
```python
@dataclass
class ProcessingConfig:
    # CSV options
    csv_delimiter: Optional[str] = None  # Auto-detect if None
    csv_encoding: Optional[str] = None  # Auto-detect if None
    csv_skip_rows: int = 0
    csv_header_row: int = 0

    # Excel options
    excel_sheet_name: Optional[str] = None  # First sheet if None
    excel_skip_rows: int = 0
    excel_header_row: int = 0

    # Normalization options
    normalize_case: bool = True
    trim_whitespace: bool = True
    handle_nulls: str = "empty"  # "empty", "null", "drop"

    # Performance options
    chunk_size: int = 10000  # For large files
    max_memory_mb: int = 512
```

### Comparison Configuration
```python
@dataclass
class ComparisonConfig:
    # Text comparison
    case_sensitive: bool = False
    ignore_whitespace: bool = True
    ignore_special_chars: bool = False

    # Numeric comparison
    float_tolerance: float = 1e-9
    percentage_tolerance: float = 0.01

    # Column selection
    compare_columns: List[str] = field(default_factory=lambda: ["*"])
    ignore_columns: List[str] = field(default_factory=list)

    # Row handling
    ignore_row_order: bool = True
    ignore_duplicate_rows: bool = False

    # Sensitivity
    sensitivity: str = "medium"  # "low", "medium", "high"
```

## Error Handling

### Processing Errors
```python
class ProcessingError(Exception):
    def __init__(self, message: str, error_code: str, details: dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}

# Error types
FILE_TOO_LARGE = "FILE_TOO_LARGE"
UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
CORRUPTED_FILE = "CORRUPTED_FILE"
ENCODING_ERROR = "ENCODING_ERROR"
PARSING_ERROR = "PARSING_ERROR"
MEMORY_LIMIT = "MEMORY_LIMIT"
```

### Recovery Strategies
1. **Encoding Fallback**: Try multiple encodings
2. **Format Fallback**: Alternative parsing methods
3. **Partial Processing**: Process valid portions
4. **Memory Management**: Chunked processing for large files
5. **Graceful Degradation**: Provide best-effort results

## Performance Optimization

### Memory Management
- Streaming for large files (>10MB)
- Chunked processing with configurable chunk sizes
- Garbage collection optimization
- Memory usage monitoring

### Processing Speed
- Parallel processing for multiple files
- Optimized pandas operations
- Caching of processed results
- Lazy loading for large datasets

### Scalability
- Async processing for I/O operations
- Background task processing
- Progress tracking and reporting
- Resource usage monitoring

## Testing and Validation

### Unit Tests
```python
class TestFileProcessor:
    def test_csv_processing(self):
        # Test various CSV formats
        pass

    def test_excel_processing(self):
        # Test different Excel versions
        pass

    def test_pdf_processing(self):
        # Test PDF extraction methods
        pass

    def test_error_handling(self):
        # Test error scenarios
        pass
```

### Integration Tests
- End-to-end file processing
- Large file handling
- Concurrent processing
- Error recovery

### Performance Tests
- Processing speed benchmarks
- Memory usage validation
- Scalability testing
- Stress testing

## Future Enhancements

### Additional File Formats
- Google Sheets integration
- JSON/XML processing
- Database imports
- API data sources

### Advanced Features
- Machine learning data classification
- Automated data cleaning
- Schema inference
- Data quality scoring

### Performance Improvements
- GPU acceleration for large datasets
- Distributed processing
- Advanced caching strategies
- Real-time processing

## Related Documentation
- Project Architecture: `system/project_architecture.md`
- API Endpoints: `system/api_endpoints.md`
- Development Workflow: `sops/file_comparison_dev_workflow.md`