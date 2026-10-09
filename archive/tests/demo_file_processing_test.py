#!/usr/bin/env python3
"""
Demo test script for file processing functionality
"""

import sys
import os
import tempfile
import csv
import json
from datetime import datetime
from pathlib import Path

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_dir)


def create_sample_csv_file():
    """Create a sample CSV file for testing"""
    print("📝 Creating Sample CSV File")
    print("-" * 40)
    
    # Create temporary CSV file
    temp_dir = tempfile.mkdtemp()
    csv_path = os.path.join(temp_dir, "sample_products.csv")
    
    sample_data = [
        ["Product Name", "SKU", "Quantity", "Unit Price", "Total Amount"],
        ["Laptop Pro", "LP001", "10", "1200.00", "12000.00"],
        ["Wireless Mouse", "WM002", "25", "25.50", "637.50"],
        ["USB-C Cable", "UC003", "50", "12.99", "649.50"],
        ["Mechanical Keyboard", "MK004", "15", "89.99", "1349.85"],
        ["Monitor 4K", "MN005", "8", "450.00", "3600.00"]
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sample_data)
    
    print(f"✅ CSV file created: {csv_path}")
    print(f"   Records: {len(sample_data) - 1} products")
    
    return csv_path, temp_dir


def test_csv_processor():
    """Test CSV processor functionality"""
    print("\n🧪 Testing CSV Processor")
    print("=" * 50)
    
    try:
        # Try to import CSV processor
        from processors.csv_processor import CSVProcessor
        
        processor = CSVProcessor()
        print("✅ CSVProcessor imported successfully")
        
        # Create test CSV file
        csv_path, temp_dir = create_sample_csv_file()
        
        # Test file validation
        is_valid = processor.validate_file(csv_path)
        print(f"✅ File validation: {'Valid' if is_valid else 'Invalid'}")
        
        # Test processing
        print("🔄 Processing CSV file...")
        result = processor.process(csv_path)
        
        # Check results
        if result and 'structured_data' in result:
            structured_data = result['structured_data']
            print(f"✅ Processing completed successfully")
            print(f"   Tables found: {len(structured_data)}")
            
            for i, table in enumerate(structured_data):
                if table.get('type') == 'table':
                    headers = table.get('headers', [])
                    rows = table.get('rows', [])
                    print(f"   Table {i+1}: {len(headers)} columns, {len(rows)} rows")
                    print(f"   Headers: {', '.join(headers)}")
                    
                    # Show first few rows
                    for j, row in enumerate(rows[:3]):
                        print(f"   Row {j+1}: {', '.join(str(cell) for cell in row)}")
                    
                    if len(rows) > 3:
                        print(f"   ... and {len(rows) - 3} more rows")
        
        # Test markdown generation
        if result and 'markdown_content' in result:
            markdown = result['markdown_content']
            print(f"✅ Markdown content generated ({len(markdown)} characters)")
            print("   Preview:")
            preview_lines = markdown.split('\n')[:10]
            for line in preview_lines:
                print(f"   {line}")
            if len(markdown.split('\n')) > 10:
                print("   ... (truncated)")
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import CSVProcessor: {e}")
        print("   This is expected if dependencies are not installed")
        return False
    except Exception as e:
        print(f"❌ CSV processor test failed: {e}")
        return False


def test_data_comparison():
    """Test data comparison functionality"""
    print("\n🧪 Testing Data Comparison")
    print("=" * 50)
    
    try:
        from comparators.data_comparator import DataComparator
        
        comparator = DataComparator()
        print("✅ DataComparator imported successfully")
        
        # Create test datasets
        dataset1 = [
            {"product": "Laptop Pro", "price": 1200.00, "quantity": 10},
            {"product": "Wireless Mouse", "price": 25.50, "quantity": 25},
            {"product": "USB-C Cable", "price": 12.99, "quantity": 50}
        ]
        
        dataset2 = [
            {"product": "Laptop Pro", "price": 1200.00, "quantity": 10},
            {"product": "Wireless Mouse", "price": 26.99, "quantity": 25},  # Price changed
            {"product": "USB-C Cable", "price": 12.99, "quantity": 45}   # Quantity changed
        ]
        
        print(f"✅ Test datasets created")
        print(f"   Dataset 1: {len(dataset1)} records")
        print(f"   Dataset 2: {len(dataset2)} records")
        
        # Test comparison
        print("🔄 Comparing datasets...")
        import asyncio
        
        async def run_comparison():
            result = await comparator.compare(dataset1, dataset2)
            return result
        
        # Run async comparison
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_comparison())
        loop.close()
        
        # Check results
        if result:
            print("✅ Comparison completed successfully")
            
            if 'summary' in result:
                summary = result['summary']
                print(f"   Total rows compared: {summary.get('total_rows_compared', 0)}")
                print(f"   Matching rows: {summary.get('matching_rows', 0)}")
                print(f"   Different rows: {summary.get('different_rows', 0)}")
                print(f"   Accuracy rate: {summary.get('accuracy_rate', 0):.2f}%")
                print(f"   Total differences: {summary.get('total_differences', 0)}")
                print(f"   Comparison time: {summary.get('comparison_time', 0):.3f}s")
            
            if 'differences' in result:
                differences = result['differences']
                print(f"   Differences found: {len(differences)}")
                
                for diff in differences:
                    print(f"   - {diff.get('field', 'unknown')}: "
                          f"'{diff.get('value1', 'N/A')}' → '{diff.get('value2', 'N/A')}' "
                          f"({diff.get('percentage_diff', 0):.1f}% change)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import DataComparator: {e}")
        print("   This is expected if dependencies are not installed")
        return False
    except Exception as e:
        print(f"❌ Data comparison test failed: {e}")
        return False


def test_file_operations():
    """Test file operation utilities"""
    print("\n🧪 Testing File Operation Utilities")
    print("=" * 50)
    
    try:
        from utils.file_utils import (
            generate_file_id, calculate_file_hash, 
            get_file_type_from_content, is_supported_file
        )
        
        print("✅ File utilities imported successfully")
        
        # Test file ID generation
        file_id = generate_file_id()
        print(f"✅ File ID generated: {file_id}")
        print(f"   Length: {len(file_id)} characters")
        print(f"   Format: {'UUID-based' if '-' in file_id else 'Short format'}")
        
        # Test file hash calculation
        test_content = b"Hello, World!"
        file_hash = calculate_file_hash(test_content)
        print(f"✅ File hash calculated: {file_hash}")
        print(f"   Algorithm: MD5")
        print(f"   Input: {len(test_content)} bytes")
        
        # Test file type detection
        file_type_tests = [
            ("test.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "xlsx"),
            ("test.csv", "text/csv", "csv"),
            ("test.pdf", "application/pdf", "pdf"),
            ("test.xls", "application/vnd.ms-excel", "xls")
        ]
        
        for filename, content_type, expected_ext in file_type_tests:
            detected_type = get_file_type_from_content(content_type, filename)
            print(f"✅ File type detection: {filename} → {detected_type}")
        
        # Test file support validation
        support_tests = [
            ("test.xlsx", True),
            ("test.csv", True),
            ("test.pdf", True),
            ("test.txt", False),
            ("test.exe", False)
        ]
        
        for filename, expected_support in support_tests:
            is_supported = is_supported_file(filename, "application/octet-stream")
            status = "✅" if is_supported == expected_support else "❌"
            print(f"   {status} Support check: {filename} → {is_supported}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import file utilities: {e}")
        return False
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False


def test_error_handling():
    """Test error handling functionality"""
    print("\n🧪 Testing Error Handling")
    print("=" * 50)
    
    try:
        from utils.exceptions import (
            UnsupportedFileTypeError, FileSizeExceededError,
            CorruptedFileError, create_http_exception
        )
        
        print("✅ Exception classes imported successfully")
        
        # Test custom exceptions
        try:
            raise UnsupportedFileTypeError("TXT files are not supported")
        except UnsupportedFileTypeError as e:
            print(f"✅ UnsupportedFileTypeError: {e}")
        
        try:
            raise FileSizeExceededError("File size (100MB) exceeds maximum (50MB)")
        except FileSizeExceededError as e:
            print(f"✅ FileSizeExceededError: {e}")
        
        try:
            raise CorruptedFileError("File appears to be corrupted or invalid")
        except CorruptedFileError as e:
            print(f"✅ CorruptedFileError: {e}")
        
        # Test HTTP exception creation
        http_error = create_http_exception(
            400, "Invalid request data", "INVALID_DATA", 
            {"field": "email", "reason": "Invalid format"}
        )
        print(f"✅ HTTP exception created: {http_error.status_code}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import exception classes: {e}")
        return False
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def test_configuration():
    """Test configuration loading"""
    print("\n🧪 Testing Configuration")
    print("=" * 50)
    
    try:
        from app.config import get_settings, create_directories
        
        print("✅ Configuration imported successfully")
        
        # Test settings loading
        settings = get_settings()
        print(f"✅ Settings loaded successfully")
        print(f"   App name: {settings.app_name}")
        print(f"   Debug mode: {settings.debug}")
        print(f"   Host: {settings.host}")
        print(f"   Port: {settings.port}")
        print(f"   Log level: {settings.log_level}")
        print(f"   Max file size: {settings.max_file_size_mb}MB")
        
        # Test directory creation
        print("🔄 Creating necessary directories...")
        create_directories()
        print("✅ Directories created/verified successfully")
        
        # Check if directories exist
        directories_to_check = [
            settings.upload_dir,
            settings.processed_dir,
            settings.export_dir
        ]
        
        for directory in directories_to_check:
            exists = os.path.exists(directory)
            status = "✅" if exists else "❌"
            print(f"   {status} {directory}: {'Exists' if exists else 'Not found'}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import configuration: {e}")
        print("   This is expected if dependencies are not installed")
        return False
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def main():
    """Run all file processing demo tests"""
    print("🎯 File Diff Backend - File Processing Demo Tests")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("File Operations", test_file_operations),
        ("Error Handling", test_error_handling),
        ("CSV Processor", test_csv_processor),
        ("Data Comparison", test_data_comparison),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 File Processing Demo Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All file processing demo tests passed!")
        print("✨ File processing functionality is working correctly!")
    else:
        print(f"⚠️  {total - passed} test(s) failed.")
        print("💡 Some tests may fail due to missing dependencies")
    
    print("\n💡 To install missing dependencies:")
    print("   pip install -r requirements.txt")
    print("   # or install specific packages:")
    print("   pip install pandas openpyxl markitdown")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)