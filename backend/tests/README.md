# Test Suite Documentation

## 📁 Cấu trúc Test

```
backend/tests/
├── conftest.py                    # Configuration và fixtures chung
├── test_core_functionality.py     # Unit tests cho core functionality
├── test_api_endpoints.py         # Integration tests cho API endpoints
└── run_tests.py                  # Test runner script
```

## 🚀 Chạy Tests

### Tất cả tests
```bash
# Chạy tất cả tests
python run_tests.py

# Chạy với coverage
python run_tests.py --coverage

# Chạy verbose mode
python run_tests.py --verbose
```

### Unit tests (Nhanh)
```bash
# Chỉ chạy unit tests
python run_tests.py --unit

# Chạy logging tests
python run_tests.py --logging

# Chạy processor tests  
python run_tests.py --processor

# Chạy comparison tests
python run_tests.py --comparison
```

### Integration tests
```bash
# Chỉ chạy integration tests
python run_tests.py --integration

# Chỉ chạy API tests
python run_tests.py --api
```

### Performance tests
```bash
# Chạy performance tests
python run_tests.py --performance

# Chạy tests nhanh (bỏ slow tests)
python run_tests.py --fast
```

## 🏷️ Test Markers

- `@pytest.mark.unit`: Unit tests (nhanh, không phụ thuộc external)
- `@pytest.mark.integration`: Integration tests (có thể cần external services)
- `@pytest.mark.slow`: Tests chạy chậm
- `@pytest.mark.logging`: Tests cho logging functionality
- `@pytest.mark.api`: Tests cho API endpoints
- `@pytest.mark.processor`: Tests cho file processors
- `@pytest.mark.comparison`: Tests cho comparison logic

## 📊 Test Coverage

```bash
# Tạo coverage report
python run_tests.py --coverage

# Xem coverage report (sau khi chạy với --coverage)
open htmlcov/index.html
```

## 🛠️ Test Categories

### 1. Unit Tests (`test_core_functionality.py`)
- **ProcessLogger Tests**: Test process tracking functionality
- **Logging Utilities Tests**: Test formatters và utilities
- **BaseProcessor Tests**: Test file processor base class
- **BaseComparator Tests**: Test comparison logic base class

### 2. Integration Tests (`test_api_endpoints.py`)
- **File Upload API**: Test upload, validation, processing
- **Comparison API**: Test file comparison endpoints
- **Health Check API**: Test system health endpoints

## 🔧 Test Fixtures

### Mock Data Fixtures
- `mock_file_data`: Mock file information
- `mock_structured_data`: Mock structured data from files
- `mock_comparison_result`: Mock comparison results
- `mock_user`: Mock authenticated user
- `temp_file`: Temporary file for testing

### Utility Fixtures  
- `test_data_factory`: Factory for creating test data
- `mock_logger`: Mock logger instance
- `sample_log_entries`: Sample log entries for testing

## 📝 Test Examples

### Unit Test Example
```python
@pytest.mark.unit
@pytest.mark.logging
class TestProcessLogger:
    def test_start_process(self):
        logger = ProcessLogger("test_module")
        process_id = logger.start_process("test_process")
        assert process_id is not None
        assert len(process_id) == 8
```

### Integration Test Example
```python
@pytest.mark.integration
@pytest.mark.api
class TestFileUploadAPI:
    def test_file_upload_success(self, client, mock_user):
        response = client.post(
            "/api/files/upload",
            files={"file": ("test.xlsx", content, content_type)},
            headers={"Authorization": "Bearer token"}
        )
        assert response.status_code == 200
```

## 🌍 Environment Variables cho Testing

```bash
# Set test environment
export TESTING=true

# Use test database  
export DATABASE_URL=sqlite:///./test.db

# Set test log level
export LOG_LEVEL=DEBUG

# Use test directories
export UPLOAD_DIR=./test_uploads
export PROCESSED_DIR=./test_processed
```

## 🔍 Debugging Tests

### Run individual test file
```bash
# Run unit tests
pytest tests/test_core_functionality.py -v

# Run API tests
pytest tests/test_api_endpoints.py -v

# Run specific test class
pytest tests/test_core_functionality.py::TestProcessLogger -v

# Run specific test method
pytest tests/test_core_functionality.py::TestProcessLogger::test_start_process -v
```

### Run with debugging output
```bash
# Verbose output
pytest -v --tb=long

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l
```

## 📈 Performance Testing

```bash
# Run performance tests
python run_tests.py --performance

# Run with benchmarking
pytest -m slow --benchmark-only
```

## 🔄 Continuous Integration

Test suite được thiết kế cho CI/CD:

```yaml
# GitHub Actions example
- name: Run Tests
  run: |
    python run_tests.py --unit --coverage
    python run_tests.py --integration
    
- name: Upload Coverage
  uses: codecov/codecov-action@v1
  with:
    file: ./coverage.xml
```

## ✅ Best Practices

1. **Naming**: Test methods nên bắt đầu với `test_`
2. **Fixtures**: Sử dụng fixtures cho data và mock objects
3. **Markers**: Sử dụng appropriate markers cho test categorization
4. **Mocking**: Mock external dependencies trong unit tests
5. **Cleanup**: Sử dụng fixtures với automatic cleanup
6. **Documentation**: Document test purpose và expected behavior
7. **Isolation**: Tests nên độc lập, không phụ thuộc lẫn nhau

## 🚨 Troubleshooting

### Common Issues

1. **Import Error**: Kiểm tra PYTHONPATH và sys.path
2. **Mock Not Working**: Đảm bảo mock được setup trước test execution
3. **Fixture Not Found**: Kiểm tra fixture naming và scope
4. **Coverage Issues**: Kiểm tra `.coveragerc` file và exclude patterns

### Debug Commands
```bash
# Check pytest configuration
pytest --version
pytest --collect-only

# Check test discovery
pytest --collect-only -q

# Dry run (không execute tests)
pytest --collect-only
```