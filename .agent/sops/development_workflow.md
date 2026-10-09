# 📖 Development Workflow Guide

## 📋 Overview

This guide outlines the standard operating procedures for developing, testing, and maintaining the File Comparison System. Following these guidelines ensures code quality, consistency, and efficient collaboration.

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** (tested with Python 3.13)
- **Git** for version control
- **Code Editor**: VS Code recommended (with Python extensions)
- **Modern Web Browser** for frontend testing

### Environment Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd File_Diff
   ```

2. **Backend Setup**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Copy environment file
   cp .env.example .env
   ```

3. **Verify Installation**
   ```bash
   # Run test suite
   python test_backend.py
   python test_sample_files.py
   ```

## 🏗️ Development Workflow

### 1. Feature Development Workflow

#### Step 1: Planning
- Check [Tasks/](../Tasks/) for existing specifications
- Create or update feature specification
- Review current system architecture in [System/](../System/)
- Identify affected components

#### Step 2: Implementation
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Implement changes
# Follow coding standards below
# Update tests as needed
```

#### Step 3: Testing
```bash
# Run comprehensive test suite
python backend/test_backend.py
python backend/test_sample_files.py
python backend/test_sample_processing.py

# If pytest is available
pytest

# Type checking
mypy backend/
```

#### Step 4: Code Quality
```bash
# Format code
black backend/
isort backend/

# Run linting
flake8 backend/ --max-line-length=88
```

#### Step 5: Documentation
- Update relevant documentation in [.agent/](../)
- Update API documentation if endpoints changed
- Update README if major changes

#### Step 6: Commit
```bash
# Stage changes
git add .

# Commit with detailed message
git commit -m "feat: add new comparison algorithm

- Implements tolerance-based numerical comparison
- Adds configurable comparison options
- Updates API with new parameters
- Includes comprehensive tests

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push and create PR
git push origin feature/your-feature-name
```

### 2. Bug Fix Workflow

#### Bug Report Template
```markdown
## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., macOS, Windows, Linux]
- Python Version: [e.g., 3.13]
- Browser: [if frontend issue]

## Additional Context
[Logs, screenshots, etc.]
```

#### Bug Fix Process
1. Create issue with detailed description
2. Reproduce bug with test case
3. Implement fix
4. Add regression tests
5. Verify fix with test suite
6. Update documentation if needed

## 📝 Coding Standards

### Python (Backend)

#### Style Guidelines
- **Maximum Line Length**: 88 characters
- **Indentation**: 4 spaces (no tabs)
- **Imports**: Organized with isort
- **Docstrings**: Google style for functions/classes
- **Type Hints**: Required for all function parameters and returns

#### Code Structure Example
```python
"""Module docstring describing purpose."""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ExampleModel(BaseModel):
    """Model for example data.
    
    Attributes:
        id: Unique identifier
        name: Display name
        created_at: Timestamp of creation
    """
    
    id: str
    name: str
    created_at: datetime
    
    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


async def process_data(
    input_data: Dict[str, any],
    options: Optional[Dict[str, any]] = None
) -> List[Dict[str, any]]:
    """Process input data with optional configurations.
    
    Args:
        input_data: Dictionary containing data to process
        options: Optional processing configurations
        
    Returns:
        List of processed data items
        
    Raises:
        ValueError: If input data is invalid
        ProcessingError: If processing fails
    """
    try:
        logger.info(f"Processing {len(input_data)} items")
        # Implementation here
        return []
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise ProcessingError(f"Failed to process data: {e}")
```

#### Error Handling
- Use custom exceptions from `utils.exceptions`
- Log errors with structured logging
- Return meaningful error messages
- Never expose sensitive data in errors

#### Performance Guidelines
- Use async/await for I/O operations
- Implement proper resource cleanup
- Add performance logging for critical operations
- Consider memory usage for large files

### Frontend (JavaScript)

#### Style Guidelines
- **ES6+**: Use modern JavaScript features
- **Indentation**: 2 spaces
- **Naming**: camelCase for variables, PascalCase for classes
- **Comments**: JSDoc for functions

#### Code Structure Example
```javascript
/**
 * Handles file upload and validation.
 * @class FileUploadHandler
 */
class FileUploadHandler {
  /**
   * Initialize file upload handler.
   * @param {HTMLElement} container - Upload container element
   * @param {Object} options - Configuration options
   */
  constructor(container, options = {}) {
    this.container = container;
    this.options = { ...this.defaultOptions, ...options };
    this.setupEventListeners();
  }

  /**
   * Setup drag and drop event listeners.
   * @private
   */
  setupEventListeners() {
    this.container.addEventListener('dragover', this.handleDragOver.bind(this));
    this.container.addEventListener('drop', this.handleDrop.bind(this));
  }

  /**
   * Handle file drop event.
   * @param {DragEvent} event - Drop event
   * @async
   */
  async handleDrop(event) {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    
    try {
      await this.processFiles(files);
    } catch (error) {
      this.showError('Failed to process files');
      console.error('File processing error:', error);
    }
  }
}
```

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for API endpoints
├── fixtures/       # Test data and sample files
└── conftest.py     # Test configuration
```

### Test Categories

#### 1. Unit Tests
- Test individual functions and classes
- Mock external dependencies
- Cover edge cases and error conditions
- Aim for 90%+ coverage

#### 2. Integration Tests
- Test API endpoints with real requests
- Test file processing with sample files
- Test database operations
- Validate complete workflows

#### 3. Performance Tests
- Test with large files (>10MB)
- Test concurrent operations
- Memory usage monitoring
- Response time validation

### Test Writing Guidelines

#### Test Structure
```python
import pytest
from unittest.mock import Mock, patch

class TestFileProcessor:
    """Test file processing functionality."""
    
    @pytest.fixture
    def sample_csv_file(self):
        """Create sample CSV file for testing."""
        return "test_file.csv"
    
    @pytest.mark.asyncio
    async def test_csv_processing_success(self, sample_csv_file):
        """Test successful CSV processing."""
        processor = CSVProcessor()
        
        result = await processor.process(sample_csv_file)
        
        assert result is not None
        assert "structured_data" in result
        assert len(result["structured_data"]) > 0
        assert result["processing_time"] > 0
    
    @pytest.mark.asyncio
    async def test_csv_processing_invalid_file(self):
        """Test processing of invalid CSV file."""
        processor = CSVProcessor()
        
        with pytest.raises(ProcessingFailedError):
            await processor.process("nonexistent.csv")
```

#### Test Data Management
- Use fixtures for reusable test data
- Clean up test files after tests
- Use parameterized tests for multiple scenarios
- Store sample files in `samples/` directory

## 🔧 Development Tools

### Recommended VS Code Extensions
- **Python**: Python extension by Microsoft
- **Python Docstring Generator**: autoDocstring
- **Python Type Hinting**: Pylance
- **GitLens**: Git history and annotations
- **ESLint**: JavaScript linting
- **Prettier**: Code formatting

### Git Configuration
```bash
# Set up Git hooks
git config core.autocrlf input
git config core.eol lf

# Set up commit signing (optional)
git config commit.gpgsign true
```

### Environment Management
```bash
# Use Python virtual environments
python -m venv venv
source venv/bin/activate

# Use direnv for automatic environment activation (optional)
echo "source venv/bin/activate" > .envrc
direnv allow
```

## 📚 Documentation Standards

### Documentation Updates
- **Always update documentation after implementing features**
- **Keep docs in sync with code changes**
- **Use clear, concise language**
- **Include code examples where helpful**

### Documentation Types
1. **API Documentation**: Auto-generated OpenAPI docs
2. **Architecture Documentation**: System design and flow
3. **SOP Documentation**: Development procedures
4. **User Documentation**: End-user guides

### Writing Guidelines
- Use Markdown for all documentation
- Include Table of Contents for longer documents
- Use semantic versioning for reference
- Link related documents
- Keep examples up-to-date

## 🚀 Deployment Procedures

### Development Deployment
```bash
# Local development
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing Deployment
```bash
# Production-like environment
export DEBUG=false
export LOG_LEVEL=INFO
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Production Deployment Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Health checks passing
- [ ] Backup procedures in place
- [ ] Monitoring configured

## 🔍 Troubleshooting

### Common Issues

#### Backend Issues
1. **Import Errors**: Check virtual environment activation
2. **Database Errors**: Verify database connection and permissions
3. **File Processing Errors**: Check file permissions and formats
4. **Performance Issues**: Monitor memory and CPU usage

#### Testing Issues
1. **Test Failures**: Check test data and fixtures
2. **Import Errors**: Verify PYTHONPATH configuration
3. **Timeout Errors**: Increase test timeouts for slow operations

### Debugging Tools
- **Logging**: Structured JSON logging with process tracking
- **Debug Mode**: Set `DEBUG=true` in environment
- **Profiling**: Use `cProfile` for performance analysis
- **Memory Debugging**: Use `memory-profiler` for memory analysis

---

**Last Updated**: 2025-10-13  
**Version**: 1.0.0  
**Maintainer**: Development Team