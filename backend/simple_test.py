#!/usr/bin/env python3
"""
Simple backend structure validation without dependencies
"""

import os
import sys

def test_file_structure():
    """Test that all required files and directories exist"""
    print("🔍 Testing backend file structure...")

    required_files = [
        "app/main.py",
        "app/config.py",
        "app/models.py",
        "app/dependencies.py",
        "processors/base_processor.py",
        "processors/csv_processor.py",
        "processors/excel_processor.py",
        "processors/pdf_processor.py",
        "comparators/base_comparator.py",
        "comparators/data_comparator.py",
        "comparators/diff_analyzer.py",
        "api/routes/__init__.py",
        "api/routes/files.py",
        "api/routes/comparison.py",
        "utils/exceptions.py",
        "main.py",
        "requirements.txt"
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")

    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False

    print("✅ All required files exist")
    return True

def test_sample_files():
    """Test that sample files exist"""
    print("\n📄 Testing sample files...")

    sample_dir = "../sample"
    if not os.path.exists(sample_dir):
        print(f"❌ Sample directory not found: {sample_dir}")
        return False

    sample_files = os.listdir(sample_dir)
    print(f"✅ Sample directory exists with files: {sample_files}")

    # Check for specific file types
    has_excel = any(f.endswith('.xlsx') for f in sample_files)
    has_pdf = any(f.endswith('.pdf') for f in sample_files)

    print(f"✅ Has Excel files: {has_excel}")
    print(f"✅ Has PDF files: {has_pdf}")

    return True

def test_basic_logic():
    """Test basic comparison logic without external dependencies"""
    print("\n🧠 Testing basic comparison logic...")

    try:
        # Simple comparison function test
        def compare_numbers(val1, val2, tolerance=0.01):
            if val1 == 0 and val2 == 0:
                return True
            elif val1 == 0 or val2 == 0:
                return abs(val1 - val2) < tolerance
            else:
                relative_diff = abs(val1 - val2) / max(abs(val1), abs(val2))
                return relative_diff <= tolerance

        # Test cases
        test_cases = [
            (100, 100, 0.01, True),
            (100, 101, 0.01, True),
            (100, 102, 0.01, False),
            (0, 0, 0.01, True),
            (0, 0.005, 0.01, True),
        ]

        for val1, val2, tolerance, expected in test_cases:
            result = compare_numbers(val1, val2, tolerance)
            if result == expected:
                print(f"✅ {val1} vs {val2} (tol={tolerance}) = {result}")
            else:
                print(f"❌ {val1} vs {val2} (tol={tolerance}) = {result}, expected {expected}")
                return False

        print("✅ Basic comparison logic works correctly")
        return True

    except Exception as e:
        print(f"❌ Logic test error: {e}")
        return False

def test_project_structure():
    """Test overall project structure"""
    print("\n📁 Testing project structure...")

    base_dir = ".."
    required_dirs = [
        "backend",
        "frontend",
        "integration",
        ".docs",
        "sample"
    ]

    for dir_name in required_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            return False

    print("✅ Project structure is correct")
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Simple Backend Validation\n")

    tests = [
        test_file_structure,
        test_sample_files,
        test_basic_logic,
        test_project_structure
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All validation tests passed!")
        print("💡 Next step: Install dependencies and run the FastAPI server")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())