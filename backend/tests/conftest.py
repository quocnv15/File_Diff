"""
Test utilities and fixtures
"""

import pytest
import tempfile
import os
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from unittest.mock import Mock


@pytest.fixture
def mock_file_data():
    """Mock file data for testing"""
    return {
        "file_id": "test_file_123",
        "filename": "test_data.xlsx",
        "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "file_size": 1024000,
        "content": b"mock excel content",
        "md5_hash": "d41d8cd98f00b204e9800998ecf8427e"
    }


@pytest.fixture
def mock_structured_data():
    """Mock structured data for testing"""
    return [
        {
            "type": "table",
            "headers": ["description", "quantity", "unit_price", "amount"],
            "rows": [
                ["Product A", "10", "100.00", "1000.00"],
                ["Product B", "5", "50.00", "250.00"],
                ["Product C", "20", "25.00", "500.00"]
            ]
        }
    ]


@pytest.fixture
def mock_comparison_result():
    """Mock comparison result for testing"""
    return {
        "comparison_id": "test_comparison_123",
        "summary": {
            "total_rows_compared": 3,
            "matching_rows": 2,
            "different_rows": 1,
            "missing_rows": 0,
            "accuracy_rate": 66.67,
            "total_differences": 2,
            "comparison_time": 1.5
        },
        "differences": [
            {
                "row_number": 2,
                "field": "quantity",
                "value1": "5",
                "value2": "7",
                "difference": 2,
                "percentage_diff": 40.0,
                "severity": "warning"
            }
        ]
    }


@pytest.fixture
def mock_user():
    """Mock authenticated user"""
    return {
        "id": "user_123",
        "username": "testuser",
        "email": "test@example.com",
        "is_active": True,
        "created_at": datetime.now()
    }


@pytest.fixture
def temp_file(mock_file_data):
    """Create a temporary file for testing"""
    temp_path = Path(tempfile.gettempdir()) / mock_file_data["filename"]
    with open(temp_path, "wb") as f:
        f.write(mock_file_data["content"])
    yield temp_path
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def mock_logger():
    """Mock logger for testing"""
    logger = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    logger.debug = Mock()
    return logger


@pytest.fixture
def sample_log_entries():
    """Sample log entries for testing"""
    return [
        {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "event": "process_start",
            "process_id": "proc_001",
            "process_name": "file_upload",
            "filename": "test.xlsx"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "event": "process_error",
            "process_id": "proc_001",
            "error_type": "ValueError",
            "error_message": "File type not supported",
            "step": "validation"
        }
    ]


class TestDataFactory:
    """Factory for creating test data"""
    
    @staticmethod
    def create_excel_data(rows: int = 10, columns: int = 4) -> List[List[str]]:
        """Create mock Excel data"""
        headers = [f"Column_{i+1}" for i in range(columns)]
        data = [headers]
        
        for row_idx in range(rows):
            row = [f"Data_{row_idx+1}_{col+1}" for col in range(columns)]
            data.append(row)
        
        return data
    
    @staticmethod
    def create_csv_data(rows: int = 10, delimiter: str = ",") -> str:
        """Create mock CSV data"""
        headers = ["description", "quantity", "unit_price", "amount"]
        lines = [delimiter.join(headers)]
        
        for i in range(rows):
            line = delimiter.join([
                f"Product {i+1}",
                str((i + 1) * 5),
                f"{(i + 1) * 10.50:.2f}",
                f"{(i + 1) * 5 * 10.50:.2f}"
            ])
            lines.append(line)
        
        return "\n".join(lines)
    
    @staticmethod
    def create_mock_file(**overrides) -> Dict[str, Any]:
        """Create mock file data"""
        default_data = {
            "file_id": str(uuid.uuid4())[:8],
            "filename": "test_file.xlsx",
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "file_size": 1024000,
            "md5_hash": "d41d8cd98f00b204e9800998ecf8427e",
            "upload_time": datetime.now(),
            "processing_status": "uploaded"
        }
        default_data.update(overrides)
        return default_data
    
    @staticmethod
    def create_mock_comparison_result(**overrides) -> Dict[str, Any]:
        """Create mock comparison result"""
        default_data = {
            "comparison_id": str(uuid.uuid4())[:8],
            "summary": {
                "total_rows_compared": 10,
                "matching_rows": 8,
                "different_rows": 2,
                "missing_rows": 0,
                "accuracy_rate": 80.0,
                "total_differences": 2,
                "comparison_time": 1.5
            },
            "differences": []
        }
        default_data.update(overrides)
        return default_data


@pytest.fixture
def test_data_factory():
    """Provide test data factory"""
    return TestDataFactory


# Test markers registration
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests (fast, no external dependencies)")
    config.addinivalue_line("markers", "integration: Integration tests (may require external services)")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "logging: Tests for logging functionality")
    config.addinivalue_line("markers", "api: API endpoint tests")
    config.addinivalue_line("markers", "processor: File processor tests")
    config.addinivalue_line("markers", "comparison: File comparison tests")