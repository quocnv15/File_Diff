# 🚀 File Comparison Backend v1.0.0

**Production-ready FastAPI backend** for processing and comparing Excel, PDF, and CSV files with intelligent data extraction and analysis.

## ✨ Features

### 🎯 **Advanced File Processing**
- **Multi-format Support**: PDF (markitdown), Excel (.xlsx/.xls), CSV with auto-detection
- **Intelligent Parsing**: Auto-delimiter and encoding detection with chardet
- **Structured Output**: Convert to Markdown with table extraction
- **Large File Support**: Optimized processing up to 50MB (configurable)

### 🔍 **Intelligent Comparison Engine**
- **Field-level Comparison**: Tolerance-based numerical comparison
- **Multiple Algorithms**: Exact match, fuzzy comparison with customizable settings
- **Advanced Analytics**: Accuracy rates, change summaries, severity indicators
- **Comparison Types**: Products, invoices, contracts, and custom scenarios

### 📤 **Professional Export System**
- **Multiple Formats**: Excel with highlighting, PDF reports, HTML interactive reports
- **Template Support**: Standard and custom export templates
- **Customizable Content**: Full data or differences only
- **Professional Styling**: Highlighted changes and comprehensive summaries

### 🚀 **Performance & Reliability**
- **Async Processing**: Non-blocking file operations with asyncio
- **GZip Compression**: Automatic response compression
- **Structured Logging**: JSON logging with process tracking and performance metrics
- **Error Handling**: Comprehensive exception management with detailed HTTP responses
- **Health Monitoring**: Real-time system metrics and dependency status
- **Concurrent Operations**: Support for multiple simultaneous file processing

### 🛡️ **Enterprise Features**
- **Modern Dependencies**: FastAPI 0.115.0, Pydantic 2.10.2
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Type Safety**: Full type hints and mypy validation
- **Test Coverage**: Comprehensive test suite with pytest
- **Configuration Management**: Environment-based settings with validation

## Quick Start

### Prerequisites
- Python 3.8+ (tested with 3.13)
- pip package manager
- Git for cloning

### Installation

1. **Clone and navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Start development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### File Management
- `POST /api/files/upload` - Upload file
- `POST /api/files/{file_id}/process` - Process file to Markdown
- `GET /api/files/{file_id}` - Get file information
- `DELETE /api/files/{file_id}` - Delete file

### Comparison
- `POST /api/comparison/compare` - Compare two files
- `GET /api/comparison/{comparison_id}` - Get comparison results
- `GET /api/comparison/{comparison_id}/summary` - Get summary

### Export
- `POST /api/export/comparison/{comparison_id}` - Create export
- `GET /api/export/{export_id}/download` - Download export

### Utilities
- `GET /api/health` - Health check
- `GET /api/supported-formats` - Supported file formats

## 🧪 Testing

### Comprehensive Test Suite
The backend includes a comprehensive test suite covering all functionality:

```bash
# Core backend validation tests
python test_backend.py

# Sample file processing tests
python test_sample_files.py

# Sample processing with comparison logic
python test_sample_processing.py

# Run with pytest (if available)
pytest

# Run with coverage
pytest --cov=backend tests/

# Type checking
mypy .
```

### Test Results
All tests are designed to pass and validate:
- ✅ Module imports and initialization
- ✅ Configuration loading and validation
- ✅ File processors (CSV, Excel, PDF)
- ✅ Data comparison algorithms
- ✅ Error handling and validation
- ✅ Performance and logging
- ✅ API endpoints functionality

## 🏗️ Development

### Project Structure
```
backend/
├── app/                    # FastAPI application core
│   ├── main.py            # Application factory and configuration
│   ├── config.py          # Settings and environment management
│   ├── models.py          # Pydantic models and data schemas
│   └── dependencies.py    # FastAPI dependencies and middleware
├── processors/             # File processing modules
│   ├── csv_processor.py   # CSV file processing with pandas
│   ├── excel_processor.py # Excel file processing with openpyxl
│   └── pdf_processor.py    # PDF processing with markitdown
├── comparators/            # Comparison algorithms
│   ├── data_comparator.py # Main comparison engine
│   └── diff_analyzer.py    # Difference analysis and reporting
├── api/                    # API routes and middleware
│   └── routes/            # API endpoint definitions
│       ├── files.py       # File management endpoints
│       └── comparison.py  # Comparison endpoints
├── utils/                  # Utility modules
│   ├── file_utils.py      # File operations helpers
│   ├── exceptions.py      # Custom exception definitions
│   └── logger.py          # Structured logging system
├── storage/                # File storage directories
│   ├── uploads/           # Uploaded files
│   ├── processed/         # Processed data
│   └── exports/           # Generated exports
└── tests/                  # Test suite
```

### Code Quality
```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Type checking with mypy
mypy .

# Run linting
flake8 .
```

## Configuration

Key environment variables (see `.env.example`):

- `DEBUG`: Enable debug mode
- `MAX_FILE_SIZE_MB`: Maximum file size limit
- `ALLOWED_ORIGINS`: CORS allowed origins
- `PDF_PROCESSOR`: PDF processing library
- `FILE_RETENTION_HOURS`: File retention period

## Supported File Formats

- **PDF**: `.pdf` (with table and text extraction)
- **Excel**: `.xlsx`, `.xls` (multi-sheet support)
- **CSV**: `.csv` (auto-detect delimiter and encoding)

## Export Formats

- **Excel**: `.xlsx` with highlighting and charts
- **PDF**: Professional report format
- **HTML**: Interactive web report
- **CSV**: Raw data for analysis

## Docker Support

```bash
# Build image
docker build -t file-comparison-backend .

# Run container
docker run -p 8000:8000 file-comparison-backend

# Use docker-compose
docker-compose up
```

## License

[Add your license information here]