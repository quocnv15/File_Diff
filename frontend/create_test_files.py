#!/usr/bin/env python3
"""
Create test Excel files for file comparison testing
"""

import pandas as pd
import os
import sys
import subprocess

def create_test_files():
    """Create two test Excel files with slight differences"""

    # File 1 data
    data1 = [
        {
            'STT': 1,
            'Mô tả sản phẩm': 'Coated Calcium Carbonate Grade 1500T',
            'Số lượng': 55,
            'Đơn giá': 73.00,
            'Thành tiền': 4015.00
        },
        {
            'STT': 2,
            'Mô tả sản phẩm': 'Coated Calcium Carbonate Grade 10T',
            'Số lượng': 27.5,
            'Đơn giá': 81.50,
            'Thành tiền': 2241.25
        },
        {
            'STT': 3,
            'Mô tả sản phẩm': 'Uncoated Calcium Carbonate Grade 2500',
            'Số lượng': 27,
            'Đơn giá': 73.00,
            'Thành tiền': 1971.00
        },
        {
            'STT': 4,
            'Mô tả sản phẩm': 'Uncoated Calcium Carbonate Grade 2000',
            'Số lượng': 55,
            'Đơn giá': 62.00,
            'Thành tiền': 3410.00
        },
        {
            'STT': 5,
            'Mô tả sản phẩm': 'Uncoated Calcium Carbonate Grade 1500',
            'Số lượng': 27.5,
            'Đơn giá': 54.00,
            'Thành tiền': 1485.00
        }
    ]

    # File 2 data (with slight differences)
    data2 = [
        {
            'STT': 1,
            'Mô tả sản phẩm': 'Coated Calcium Carbonate Grade 1500T',
            'Số lượng': 55,
            'Đơn giá': 75.00,  # Different price
            'Thành tiền': 4125.00  # Different amount
        },
        {
            'STT': 2,
            'Mô tả sản phẩm': 'Coated Calcium Carbonate Grade 10T',
            'Số lượng': 27.5,
            'Đơn giá': 81.50,
            'Thành tiền': 2241.25
        },
        {
            'STT': 3,
            'Mô tả sản phẩm': 'Uncoated Calcium Carbonate Grade 2500',
            'Số lượng': 30,      # Different quantity
            'Đơn giá': 73.00,
            'Thành tiền': 2190.00  # Different amount
        },
        {
            'STT': 4,
            'Mô tả sản phẩm': 'Uncoated Calcium Carbonate Grade 2000',
            'Số lượng': 55,
            'Đơn giá': 62.00,
            'Thành tiền': 3410.00
        },
        {
            'STT': 5,
            'Mô tả sản phẩm': 'Uncoated Calcium Carbonate Grade 1500',
            'Số lượng': 27.5,
            'Đơn giá': 54.00,
            'Thành tiền': 1485.00
        },
        {
            'STT': 6,  # Additional item
            'Mô tả sản phẩm': 'Uncoated Calcium Carbonate Grade 1000',
            'Số lượng': 82.5,
            'Đơn giá': 50.00,
            'Thành tiền': 4125.00
        }
    ]

    # Create DataFrames
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    # Save to Excel files
    df1.to_excel('test_file1.xlsx', index=False, engine='openpyxl')
    df2.to_excel('test_file2.xlsx', index=False, engine='openpyxl')

    print("✓ Created test_file1.xlsx with 5 items")
    print("✓ Created test_file2.xlsx with 6 items (including differences)")
    print("\nDifferences:")
    print("- Item 1: Different price (73.00 → 75.00) and amount")
    print("- Item 3: Different quantity (27 → 30) and amount")
    print("- Item 6: Additional item in file 2")

    # Also create CSV versions
    df1.to_csv('test_file1.csv', index=False, encoding='utf-8-sig')
    df2.to_csv('test_file2.csv', index=False, encoding='utf-8-sig')
    print("\n✓ Also created CSV versions")

if __name__ == "__main__":
    # Check if required packages are available
    try:
        import pandas as pd
    except ImportError:
        print("Installing required packages...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Packages installed successfully")
        else:
            print(f"❌ Failed to install packages: {result.stderr}")
            sys.exit(1)
        import pandas as pd

    create_test_files()
    print(f"\nTest files created in {os.getcwd()}")