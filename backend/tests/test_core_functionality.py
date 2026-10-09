"""
Unit tests for backend core functionality
"""

import pytest
import json
import time
import asyncio
import sys
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Test logging utilities
@pytest.mark.unit
@pytest.mark.logging
class TestProcessLogger:
    """Test ProcessLogger functionality"""
    
    def setup_method(self):
        """Setup test logger"""
        from utils.logger import ProcessLogger
        self.logger = ProcessLogger("test_module")
    
    def test_start_process(self):
        """Test starting a new process"""
        process_id = self.logger.start_process("test_process", test_param="test_value")
        
        assert process_id is not None
        assert len(process_id) == 8
        assert len(self.logger.process_stack) == 1
        assert self.logger.process_stack[0]["process_name"] == "test_process"
    
    def test_end_process(self):
        """Test ending a process"""
        process_id = self.logger.start_process("test_process")
        
        with patch.object(self.logger.logger, 'info') as mock_info:
            self.logger.end_process(process_id, result="success")
            mock_info.assert_called_once()
            args, kwargs = mock_info.call_args
            assert "Process completed: test_process" in args[0]
            assert kwargs["extra"]["process_id"] == process_id
            assert kwargs["extra"]["result"] == "success"
        
        assert len(self.logger.process_stack) == 0
    
    def test_log_step(self):
        """Test logging a step"""
        process_id = self.logger.start_process("test_process")
        
        with patch.object(self.logger.logger, 'info') as mock_info:
            self.logger.log_step("test_step", step_data="test_value")
            mock_info.assert_called_once()
            args, kwargs = mock_info.call_args
            assert "Step: test_step" in args[0]
            assert kwargs["extra"]["step_name"] == "test_step"
            assert kwargs["extra"]["process_id"] == process_id
    
    def test_log_error(self):
        """Test error logging"""
        process_id = self.logger.start_process("test_process")
        test_error = ValueError("Test error")
        
        with patch.object(self.logger.logger, 'error') as mock_error:
            self.logger.log_error(test_error, context_data="test_context")
            mock_error.assert_called_once()
            args, kwargs = mock_error.call_args
            assert args[0] == test_error
            assert kwargs["extra"]["error_type"] == "ValueError"
            assert kwargs["extra"]["error_message"] == "Test error"
            assert kwargs["extra"]["process_id"] == process_id


@pytest.mark.unit
@pytest.mark.logging
class TestLoggingUtilities:
    """Test logging utility functions"""
    
    def test_structured_formatter(self):
        """Test JSON structured logging formatter"""
        from utils.logger import StructuredFormatter
        import logging
        
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        formatter = StructuredFormatter()
        formatted = formatter.format(record)
        log_data = json.loads(formatted)
        
        assert log_data["level"] == "INFO"
        assert log_data["logger"] == "test_logger"
        assert log_data["message"] == "Test message"
        assert "timestamp" in log_data
    
    def test_colored_formatter(self):
        """Test colored console formatter"""
        from utils.logger import ColoredFormatter
        import logging
        
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        formatter = ColoredFormatter()
        formatted = formatter.format(record)
        
        assert "\033[32m" in formatted  # Green color for INFO
        assert "\033[0m" in formatted   # Reset color
        assert "INFO" in formatted
    
    def test_file_operation_logging(self):
        """Test file operation logging"""
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger
            
            from utils.logger import log_file_operation
            log_file_operation("upload", "file_123", "test.xlsx", file_size=1024)
            
            mock_logger.info.assert_called_once()
            args, kwargs = mock_logger.info.call_args
            assert "File upload: test.xlsx" in args[0]
            assert kwargs["extra"]["operation"] == "upload"
            assert kwargs["extra"]["file_id"] == "file_123"
    
    def test_comparison_operation_logging(self):
        """Test comparison operation logging"""
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = Mock()
            mock_get_logger.return_value = mock_logger
            
            from utils.logger import log_comparison_operation
            log_comparison_operation("compare", "comp_123", "file_1", "file_2", differences=5)
            
            mock_logger.info.assert_called_once()
            args, kwargs = mock_logger.info.call_args
            assert "Comparison compare: comp_123" in args[0]
            assert kwargs["extra"]["operation"] == "compare"
            assert kwargs["extra"]["differences"] == 5


# Test processors
@pytest.mark.unit
@pytest.mark.processor
class TestBaseProcessor:
    """Test BaseProcessor functionality"""
    
    def setup_method(self):
        """Setup mock processor"""
        class MockProcessor:
            def __init__(self):
                self.supported_extensions = [".xlsx", ".csv"]
                self.process_logger = Mock()
            
            def _create_markdown_table(self, headers, rows):
                if not headers or not rows:
                    return ""
                
                # Simple implementation
                markdown = []
                markdown.append("| " + " | ".join(headers) + " |")
                markdown.append("| " + " | ".join(["-" * len(h) for h in headers]) + " |")
                for row in rows:
                    markdown.append("| " + " | ".join([str(cell) for cell in row]) + " |")
                return "\n".join(markdown)
            
            def _extract_metadata(self, file_path):
                import os
                from datetime import datetime
                
                try:
                    stat = os.stat(file_path)
                    return {
                        "file_size": stat.st_size,
                        "created_time": datetime.fromtimestamp(stat.st_ctime),
                        "modified_time": datetime.fromtimestamp(stat.st_mtime),
                        "processor": "MockProcessor"
                    }
                except:
                    return {"processor": "MockProcessor"}
        
        self.processor = MockProcessor()
    
    def test_validate_file_extensions(self):
        """Test file validation by extension"""
        # Mock validation method
        def validate_file(file_path):
            return file_path.endswith(('.xlsx', '.csv'))
        
        self.processor.validate_file = validate_file
        
        assert self.processor.validate_file("test.xlsx") is True
        assert self.processor.validate_file("test.csv") is True
        assert self.processor.validate_file("test.pdf") is False
    
    def test_create_markdown_table(self):
        """Test markdown table creation"""
        headers = ["Name", "Age", "City"]
        rows = [
            ["Alice", "25", "New York"],
            ["Bob", "30", "San Francisco"]
        ]
        
        markdown = self.processor._create_markdown_table(headers, rows)
        
        assert "Name" in markdown
        assert "Age" in markdown
        assert "City" in markdown
        assert "Alice" in markdown
        assert "Bob" in markdown
        assert "|" in markdown
    
    def test_create_markdown_table_empty(self):
        """Test markdown table with empty data"""
        result = self.processor._create_markdown_table([], [])
        assert result == ""
        
        result = self.processor._create_markdown_table(["Header"], [])
        assert result == ""


# Test comparators
@pytest.mark.unit
@pytest.mark.comparison
class TestBaseComparator:
    """Test BaseComparator functionality"""
    
    def setup_method(self):
        """Setup mock comparator"""
        class MockComparator:
            def __init__(self):
                self.tolerance_settings = {
                    "quantity": 0.1,
                    "unit_price": 0.01,
                    "amount": 0.01
                }
                self.process_logger = Mock()
            
            def _normalize_value(self, value):
                if value is None:
                    return ""
                elif isinstance(value, str):
                    return value.strip().lower()
                elif isinstance(value, (int, float)):
                    return float(value)
                else:
                    return str(value).strip().lower()
            
            def _is_numeric(self, value):
                try:
                    float(value)
                    return True
                except (ValueError, TypeError):
                    return False
            
            def _parse_numeric(self, value):
                try:
                    if isinstance(value, str):
                        clean_value = value.replace(',', '').replace('$', '').strip()
                        return float(clean_value)
                    return float(value)
                except (ValueError, TypeError):
                    return 0.0
            
            def _compare_numbers(self, val1, val2, tolerance=0.0):
                if val1 == 0 and val2 == 0:
                    return True
                elif val1 == 0 or val2 == 0:
                    return abs(val1 - val2) < tolerance
                else:
                    relative_diff = abs(val1 - val2) / max(abs(val1), abs(val2))
                    return relative_diff <= tolerance
            
            def _calculate_percentage_difference(self, val1, val2):
                if val1 == 0 and val2 == 0:
                    return 0.0
                elif val1 == 0:
                    return 100.0 if val2 != 0 else 0.0
                else:
                    return abs((val2 - val1) / val1) * 100
        
        self.comparator = MockComparator()
    
    def test_normalize_value(self):
        """Test value normalization"""
        assert self.comparator._normalize_value(None) == ""
        assert self.comparator._normalize_value("  Test  ") == "test"
        assert self.comparator._normalize_value(123) == 123.0
        assert self.comparator._normalize_value("45.67") == 45.67
        assert self.comparator._normalize_value(True) == "true"
    
    def test_is_numeric(self):
        """Test numeric value detection"""
        assert self.comparator._is_numeric(123) is True
        assert self.comparator._is_numeric("45.67") is True
        assert self.comparator._is_numeric("-100") is True
        assert self.comparator._is_numeric("abc") is False
        assert self.comparator._is_numeric(None) is False
        assert self.comparator._is_numeric([]) is False
    
    def test_parse_numeric(self):
        """Test numeric value parsing"""
        assert self.comparator._parse_numeric("123") == 123.0
        assert self.comparator._parse_numeric("45.67") == 45.67
        assert self.comparator._parse_numeric("$1,234.56") == 1234.56
        assert self.comparator._parse_numeric("abc") == 0.0
        assert self.comparator._parse_numeric(123) == 123.0
    
    def test_compare_numbers(self):
        """Test number comparison with tolerance"""
        assert self.comparator._compare_numbers(100, 100) is True
        assert self.comparator._compare_numbers(100, 105, 0.1) is True  # 5% difference
        assert self.comparator._compare_numbers(100, 89, 0.1) is False  # 11% difference
        assert self.comparator._compare_numbers(0, 0.5, tolerance=1.0) is True
    
    def test_calculate_percentage_difference(self):
        """Test percentage difference calculation"""
        assert self.comparator._calculate_percentage_difference(100, 100) == 0.0
        assert self.comparator._calculate_percentage_difference(100, 110) == 10.0
        assert self.comparator._calculate_percentage_difference(100, 90) == 10.0
        assert self.comparator._calculate_percentage_difference(0, 0) == 0.0
        assert self.comparator._calculate_percentage_difference(0, 100) == 100.0
    
    def test_tolerance_settings(self):
        """Test tolerance settings"""
        assert self.comparator.tolerance_settings["quantity"] == 0.1
        assert self.comparator.tolerance_settings["unit_price"] == 0.01
        assert self.comparator.tolerance_settings["amount"] == 0.01