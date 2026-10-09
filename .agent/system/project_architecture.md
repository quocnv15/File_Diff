# File Comparison System - Project Architecture

## 🎯 Project Overview
**Hệ Thống So Sánh File Dữ Liệu** - Vietnamese web application for comparing Excel, PDF, and CSV files with intelligent diff visualization and reporting capabilities.

## 🛠 Tech Stack

### Backend (FastAPI)
- **Framework**: FastAPI with async processing
- **Language**: Python 3.8+
- **File Processing**: pandas, openpyxl, markitdown
- **API**: RESTful with OpenAPI/Swagger docs
- **Server**: uvicorn ASGI server

### Frontend (Vanilla Web)
- **Language**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Custom components with responsive design
- **Features**: Drag & drop upload, real-time diff visualization
- **Language**: Vietnamese interface

### File Support
- **Excel**: .xlsx, .xls (openpyxl)
- **PDF**: Table extraction (markitdown + PyPDF2 fallback)
- **CSV**: Auto-delimiter/encoding detection (pandas)

### Development Environment
- **IDE**: VS Code
- **Version Control**: Git + GitHub
- **AI Assistant**: Claude Code integration
- **Testing**: Custom test scripts

## 📁 Project Structure

### Backend (FastAPI)
```
backend/
├── app/                    # Core application
│   ├── config.py          # Settings & configuration
│   ├── models.py          # Pydantic models
│   └── dependencies.py    # FastAPI dependencies
├── api/routes/            # API endpoints
│   ├── files.py          # File upload/management
│   ├── comparison.py     # Comparison operations
│   └── health.py         # System health checks
├── processors/            # File handling modules
│   ├── base_processor.py  # Abstract base class
│   ├── csv_processor.py   # CSV processing
│   ├── excel_processor.py # Excel processing
│   └── pdf_processor.py   # PDF processing
├── comparators/           # Comparison engine
│   ├── base_comparator.py # Base comparison logic
│   └── diff_analyzer.py   # Difference analysis
├── utils/                 # Utility functions
│   ├── file_utils.py      # File operations
│   └── exceptions.py      # Custom exceptions
├── storage/               # File directories
│   ├── uploads/          # Uploaded files
│   ├── processed/        # Processed data
│   └── exports/          # Generated reports
└── main.py               # FastAPI entry point
```

### Frontend (Vanilla Web)
```
frontend/
├── index.html            # Main application page
├── scripts/             # JavaScript modules
│   ├── main.js          # Core application logic
│   ├── api_integration.js # Backend communication
│   ├── diff-visualization.js # Diff display
│   └── utils/           # Helper utilities
│       ├── file-parsers.js   # Client-side parsing
│       └── helpers.js        # Utility functions
├── styles/              # CSS styling
│   ├── main.css         # Primary styles
│   └── diff.css         # Diff visualization
└── assets/              # Static resources
```

## 🚀 Core Features

### File Processing
- **Multi-format support**: Excel (.xlsx, .xls), PDF, CSV
- **Intelligent parsing**: Auto-detection of delimiters, encodings
- **Data normalization**: Consistent formatting across file types
- **Error handling**: Graceful fallback and recovery

### Comparison Engine
- **Flexible algorithms**: Exact match, fuzzy matching, custom rules
- **Performance optimized**: Memory-efficient for large files
- **Configurable options**: Case sensitivity, whitespace handling
- **Smart diff detection**: Added, removed, modified content

### Visualization
- **Multiple views**: Side-by-side, unified, table format
- **Interactive navigation**: Jump between differences
- **Statistics dashboard**: Accuracy rates, change summaries
- **Responsive design**: Mobile-friendly interface

### Export Capabilities
- **Multiple formats**: Excel, PDF, HTML reports
- **Customizable content**: Full data or differences only
- **Professional formatting**: Styled reports with highlights
- **Batch processing**: Handle multiple comparisons

## 🔧 Technical Implementation

### Backend Processing
- **Async operations**: Non-blocking file I/O
- **Memory management**: Streaming for large files
- **Error recovery**: Multiple parsing strategies
- **Caching**: Results optimization

### Frontend Features
- **Progressive upload**: Real-time progress indicators
- **Client-side parsing**: Optional frontend processing
- **Interactive UI**: Dynamic content loading
- **Theme support**: Light/dark mode switching

### Integration Points
- **API communication**: RESTful endpoints
- **File handling**: Multipart uploads
- **Error propagation**: Consistent error states
- **Performance monitoring**: Processing time tracking

## 📊 Performance & Scalability

### Optimization Strategies
- **Chunked processing**: Large file handling
- **Lazy loading**: On-demand data rendering
- **Result caching**: Avoid redundant processing
- **Memory monitoring**: Resource usage tracking

### File Limits
- **Maximum size**: 100MB per file
- **Supported formats**: CSV, Excel, PDF
- **Processing time**: Optimized for speed
- **Concurrent users**: Multi-user support

## 🛠 Development Environment

### Local Setup
- **Backend server**: `localhost:8000` (FastAPI)
- **Frontend server**: Static file serving
- **CORS configuration**: Cross-origin requests enabled
- **Hot reload**: Development-friendly workflow

### Testing Framework
- **Unit tests**: Individual component testing
- **Integration tests**: API endpoint validation
- **File tests**: Comparison accuracy verification
- **Performance tests**: Speed and memory benchmarks

## 📚 Related Documentation
- **API Reference**: `system/api_endpoints.md`
- **File Processing**: `system/file_processing.md`
- **Development Workflow**: `sops/file_comparison_dev_workflow.md`
- **AI Integration**: `sops/ai_tools_integration.md`