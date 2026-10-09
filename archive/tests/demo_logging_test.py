#!/usr/bin/env python3
"""
Demo test script for logging functionality
"""

import sys
import os
import time
import uuid
from datetime import datetime

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_dir)

def test_logging_basic():
    """Test basic logging functionality"""
    print("🧪 Testing Basic Logging Functionality")
    print("=" * 50)
    
    try:
        from utils.logger import ProcessLogger, get_process_logger
        
        # Test process logger creation
        logger = get_process_logger("demo_module")
        print("✅ ProcessLogger created successfully")
        
        # Test process tracking
        process_id = logger.start_process("demo_process", test_param="demo_value")
        print(f"✅ Process started with ID: {process_id}")
        
        # Test step logging
        logger.log_step("demo_step_1", step_data="demo_data_1")
        print("✅ Step 1 logged successfully")
        
        logger.log_step("demo_step_2", step_data="demo_data_2")
        print("✅ Step 2 logged successfully")
        
        # Test process completion
        logger.end_process(process_id, result="demo_success")
        print("✅ Process completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_file_operations():
    """Test file operation logging"""
    print("\n🧪 Testing File Operation Logging")
    print("=" * 50)
    
    try:
        from utils.logger import log_file_operation
        
        # Test file upload logging
        log_file_operation(
            "upload",
            "demo_file_123",
            "demo_file.xlsx",
            file_size=1024000,
            file_type="xlsx",
            upload_time=datetime.now().isoformat()
        )
        print("✅ File upload operation logged successfully")
        
        # Test file processing logging
        log_file_operation(
            "process",
            "demo_file_123",
            "demo_file.xlsx",
            processing_time=2.5,
            tables_extracted=3,
            rows_processed=150
        )
        print("✅ File processing operation logged successfully")
        
        # Test file deletion logging
        log_file_operation(
            "delete",
            "demo_file_123",
            "demo_file.xlsx",
            deletion_reason="test_cleanup"
        )
        print("✅ File deletion operation logged successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_comparison_operations():
    """Test comparison operation logging"""
    print("\n🧪 Testing Comparison Operation Logging")
    print("=" * 50)
    
    try:
        from utils.logger import log_comparison_operation
        
        # Test comparison start logging
        log_comparison_operation(
            "compare",
            "demo_comparison_123",
            "demo_file_1",
            "demo_file_2",
            comparison_type="product_comparison"
        )
        print("✅ Comparison start logged successfully")
        
        # Test comparison completion logging
        log_comparison_operation(
            "compare_completed",
            "demo_comparison_123",
            "demo_file_1",
            "demo_file_2",
            total_rows_compared=100,
            differences_found=5,
            accuracy_rate=95.0,
            comparison_time=1.8
        )
        print("✅ Comparison completion logged successfully")
        
        # Test comparison cleanup logging
        log_comparison_operation(
            "cleanup",
            "demo_comparison_123",
            "demo_file_1",
            "demo_file_2",
            cleanup_reason="auto_cleanup",
            retention_hours=24
        )
        print("✅ Comparison cleanup logged successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_error_logging():
    """Test error logging functionality"""
    print("\n🧪 Testing Error Logging Functionality")
    print("=" * 50)
    
    try:
        from utils.logger import get_process_logger
        
        logger = get_process_logger("demo_error_module")
        process_id = logger.start_process("demo_error_process")
        
        # Test warning logging
        logger.log_warning(
            "This is a demo warning message",
            warning_type="demo_warning",
            context="demo_context"
        )
        print("✅ Warning logged successfully")
        
        # Test error logging
        try:
            # Simulate an error
            raise ValueError("This is a demo error for testing")
        except ValueError as e:
            logger.log_error(
                e,
                error_context="demo_error_context",
                user_action="demo_action"
            )
            print("✅ Error logged successfully")
        
        logger.end_process(process_id, status="completed_with_errors")
        print("✅ Error process completed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_nested_processes():
    """Test nested process logging"""
    print("\n🧪 Testing Nested Process Logging")
    print("=" * 50)
    
    try:
        from utils.logger import get_process_logger
        
        logger = get_process_logger("demo_nested_module")
        
        # Start outer process
        outer_id = logger.start_process("outer_process", outer_param="outer_value")
        print(f"✅ Outer process started: {outer_id}")
        
        # Start inner process
        inner_id = logger.start_process("inner_process", inner_param="inner_value")
        print(f"✅ Inner process started: {inner_id}")
        
        # Log steps in inner process
        logger.log_step("inner_step_1")
        logger.log_step("inner_step_2")
        
        # End inner process
        logger.end_process(inner_id, inner_result="inner_success")
        print("✅ Inner process completed")
        
        # Log steps in outer process
        logger.log_step("outer_step_1")
        logger.log_step("outer_step_2")
        
        # End outer process
        logger.end_process(outer_id, outer_result="outer_success")
        print("✅ Outer process completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_performance_logging():
    """Test performance logging with timing"""
    print("\n🧪 Testing Performance Logging")
    print("=" * 50)
    
    try:
        from utils.logger import get_process_logger
        
        logger = get_process_logger("demo_performance_module")
        
        # Test fast process
        fast_id = logger.start_process("fast_process")
        time.sleep(0.1)  # Simulate 100ms work
        logger.end_process(fast_id)
        print("✅ Fast process logged (100ms)")
        
        # Test medium process
        medium_id = logger.start_process("medium_process")
        time.sleep(0.5)  # Simulate 500ms work
        logger.end_process(medium_id)
        print("✅ Medium process logged (500ms)")
        
        # Test slow process
        slow_id = logger.start_process("slow_process")
        time.sleep(1.0)  # Simulate 1s work
        logger.end_process(slow_id)
        print("✅ Slow process logged (1s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Run all demo tests"""
    print("🎯 File Diff Backend - Logging Demo Tests")
    print("=" * 60)
    
    tests = [
        ("Basic Logging", test_logging_basic),
        ("File Operations", test_file_operations),
        ("Comparison Operations", test_comparison_operations),
        ("Error Logging", test_error_logging),
        ("Nested Processes", test_nested_processes),
        ("Performance Logging", test_performance_logging),
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
    print("📊 Demo Test Results Summary:")
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
        print("🎉 All demo tests passed!")
        print("✨ Logging system is working correctly!")
    else:
        print(f"⚠️  {total - passed} test(s) failed.")
    
    print("\n💡 Note: Check the logs above to see detailed logging output")
    print("📝 Logs show process tracking, step logging, and error handling")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)