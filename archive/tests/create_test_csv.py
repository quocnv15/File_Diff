"""
Create comprehensive CSV test files for file comparison system self-testing
"""

import os
import csv

# Create sample directory
SAMPLE_DIR = "/Volumes/Workspace/1-SideProject/File_Diff/samples"

def create_product_comparison_csv():
    """Create CSV files with product comparison data"""
    
    # Version 1 data
    products_v1 = [
        ['STT', 'Mã SP', 'Tên sản phẩm', 'Đơn vị', 'Số lượng', 'Đơn giá', 'Thành tiền'],
        [1, 'CC1500', 'Canxi Carbonate Coated Grade 1500T', 'kg', 1000, 75000, 75000000],
        [2, 'CC800', 'Canxi Carbonate Uncoated Grade 800', 'kg', 2000, 45000, 90000000],
        [3, 'TALC325', 'Bột Talc Mesh 325', 'kg', 500, 120000, 60000000],
        [4, 'TALC600', 'Bột Talc Mesh 600', 'kg', 300, 180000, 54000000],
        [5, 'KAOLIN', 'Kaolin Clay', 'kg', 800, 95000, 76000000]
    ]
    
    filename_v1 = os.path.join(SAMPLE_DIR, "product_comparisons", "product_comparison_v1.csv")
    with open(filename_v1, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(products_v1)
    
    # Version 2 data with differences
    products_v2 = [
        ['STT', 'Mã SP', 'Tên sản phẩm', 'Đơn vị', 'Số lượng', 'Đơn giá', 'Thành tiền'],
        [1, 'CC1500', 'Canxi Carbonate Coated Grade 1500T', 'kg', 1000, 78000, 78000000],  # Price changed
        [2, 'CC800', 'Canxi Carbonate Uncoated Grade 800', 'kg', 2000, 45000, 90000000],  # Same
        [3, 'TALC325', 'Bột Talc Mesh 325', 'kg', 550, 120000, 66000000],  # Quantity changed
        [4, 'TALC600', 'Bột Talc Mesh 600 Premium', 'kg', 300, 185000, 55500000],  # Name and price changed
        [6, 'CALCITE', 'Canxi Calcite', 'kg', 200, 55000, 11000000]  # New product
    ]
    
    filename_v2 = os.path.join(SAMPLE_DIR, "product_comparisons", "product_comparison_v2.csv")
    with open(filename_v2, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(products_v2)
    
    return filename_v1, filename_v2

def create_invoice_csv():
    """Create CSV files with invoice data"""
    
    # Invoice 1
    invoice1_items = [
        ['STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị', 'Số lượng', 'Đơn giá', 'Thành tiền'],
        [1, 'Canxi Carbonate Coated 1500T', 'kg', 500, 75000, 37500000],
        [2, 'Talc Powder 325 mesh', 'kg', 200, 120000, 24000000],
        [3, 'Kaolin Clay', 'kg', 100, 95000, 9500000],
        [4, 'Phí vận chuyển', 'lượt', 1, 500000, 500000]
    ]
    
    filename_invoice1 = os.path.join(SAMPLE_DIR, "invoice_comparisons", "invoice_001.csv")
    with open(filename_invoice1, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(invoice1_items)
    
    # Invoice 2 with differences
    invoice2_items = [
        ['STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị', 'Số lượng', 'Đơn giá', 'Thành tiền'],
        [1, 'Canxi Carbonate Coated 1500T', 'kg', 480, 75000, 36000000],  # Quantity changed
        [2, 'Talc Powder 325 mesh', 'kg', 200, 125000, 25000000],  # Price changed
        [3, 'Kaolin Clay Premium', 'kg', 100, 98000, 9800000],  # Name and price changed
        [4, 'Phí vận chuyển', 'lượt', 1, 450000, 450000],  # Shipping cost changed
        [5, 'Chi phí đóng gói', 'cái', 10, 50000, 500000]  # New item
    ]
    
    filename_invoice2 = os.path.join(SAMPLE_DIR, "invoice_comparisons", "invoice_002.csv")
    with open(filename_invoice2, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(invoice2_items)
    
    return filename_invoice1, filename_invoice2

def create_edge_cases_csv():
    """Create CSV file with edge cases"""
    
    edge_data = [
        ['STT', 'Mã SP', 'Tên sản phẩm', 'Mô tả', 'Số lượng', 'Đơn giá', 'Thành tiền', 'Ghi chú'],
        [1, 'SP001', 'Sản phẩm bình thường', 'Mô tả đầy đủ', 100, 50000, 5000000, 'Bình thường'],
        [2, 'SP002', 'Sản phẩm thiếu thông tin', '', '', '', '', 'Thiếu dữ liệu'],  # Empty cells
        [3, 'SP003', 'Sản phẩm ký tự đặc biệt !@#$%^&*()', 'Mô tả có dấu: Nguyễn Văn A', 5.5, 33333.33, 183333.32, 'Đặc biệt'],
        [4, '', 'Sản phẩm không có mã', 'Sản phẩm thiếu mã', -10, 100000, -1000000, 'Trả hàng'],  # Empty and negative
        [5, 'SP005', 'Sản phẩm với số 0', 'Kiểm tra giá trị 0', 0, 0, 0, 'Giá trị bằng 0'],
        [6, 'SP006', 'Sản phẩm có dấu tiếng Việt', 'Sản phẩm: Áo Đầm, Váy Công Sở', 25, 250000, 6250000, 'Tiếng Việt'],
        [7, 'SP007', 'Sản phẩm dài', 'Tên sản phẩm rất dài để kiểm tra xử lý văn bản dài trong file CSV', 1, 1000000, 1000000, 'Dài']
    ]
    
    filename = os.path.join(SAMPLE_DIR, "edge_cases", "edge_cases_csv.csv")
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(edge_data)
    
    return filename

def create_decimal_precision_csv():
    """Create CSV file to test decimal precision"""
    
    decimal_data = [
        ['STT', 'Tên sản phẩm', 'Số lượng', 'Đơn giá', 'Thành tiền', 'VAT 10%', 'Tổng cộng'],
        [1, 'Sản phẩm A', 1.123456789, 12345.6789, 13873.4457, 1387.34457, 15260.79027],
        [2, 'Sản phẩm B', 2.5, 9999.99, 24999.975, 2499.9975, 27499.9725],
        [3, 'Sản phẩm C', 0.333333, 30000, 9999.99, 999.999, 10999.989],
        [4, 'Sản phẩm D', 10.123456789, 55555.555555, 562777.654321, 56277.765432, 619055.419753]
    ]
    
    filename = os.path.join(SAMPLE_DIR, "decimal_tests", "decimal_precision_csv.csv")
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(decimal_data)
    
    return filename

def create_different_delimiters_csv():
    """Create CSV files with different delimiters"""
    
    # Semicolon delimiter
    semicolon_data = [
        ['STT;Mã SP;Tên sản phẩm;Số lượng;Đơn giá;Thành tiền'],
        ['1;SP001;Sản phẩm A;100;50000;5000000'],
        ['2;SP002;Sản phẩm B;200;75000;15000000']
    ]
    
    filename_semicolon = os.path.join(SAMPLE_DIR, "edge_cases", "semicolon_delimiter.csv")
    with open(filename_semicolon, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(semicolon_data)
    
    # Tab delimiter
    tab_data = [
        ['STT\tMã SP\tTên sản phẩm\tSố lượng\tĐơn giá\tThành tiền'],
        ['1\tSP001\tSản phẩm A\t100\t50000\t5000000'],
        ['2\tSP002\tSản phẩm B\t200\t75000\t15000000']
    ]
    
    filename_tab = os.path.join(SAMPLE_DIR, "edge_cases", "tab_delimiter.csv")
    with open(filename_tab, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(tab_data)
    
    return filename_semicolon, filename_tab

def create_large_dataset_csv():
    """Create large CSV file for performance testing"""
    
    # Generate 1000 rows of test data
    header = ['STT', 'Mã SP', 'Tên sản phẩm', 'Danh mục', 'Số lượng', 'Đơn giá', 'Thành tiền', 'Nhà cung cấp', 'Ghi chú']
    
    large_data = [header]
    
    categories = ['Hóa chất', 'Vật liệu xây dựng', 'Nông sản', 'Thực phẩm', 'Dược phẩm']
    suppliers = ['Nhà cung cấp A', 'Nhà cung cấp B', 'Nhà cung cấp C', 'Nhà cung cấp D']
    
    for i in range(1, 1001):
        row = [
            i,
            f'SP{i:04d}',
            f'Sản phẩm mẫu số {i}',
            categories[i % len(categories)],
            random.randint(1, 1000),
            random.randint(10000, 500000),
            random.randint(10000, 500000000),
            suppliers[i % len(suppliers)],
            f'Ghi chú cho sản phẩm {i}'
        ]
        large_data.append(row)
    
    filename = os.path.join(SAMPLE_DIR, "edge_cases", "large_dataset_1000rows.csv")
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(large_data)
    
    return filename

if __name__ == "__main__":
    import random
    
    print("Creating CSV test files for comprehensive self-testing...")
    
    files_created = []
    
    try:
        # Product comparison files
        prod1, prod2 = create_product_comparison_csv()
        files_created.extend([prod1, prod2])
        
        # Invoice files
        inv1, inv2 = create_invoice_csv()
        files_created.extend([inv1, inv2])
        
        # Edge cases file
        files_created.append(create_edge_cases_csv())
        
        # Decimal precision file
        files_created.append(create_decimal_precision_csv())
        
        # Different delimiters
        delim1, delim2 = create_different_delimiters_csv()
        files_created.extend([delim1, delim2])
        
        # Large dataset
        files_created.append(create_large_dataset_csv())
        
        print(f"\n✅ Successfully created {len(files_created)} CSV test files:")
        for file in files_created:
            print(f"   📄 {os.path.basename(file)}")
        
        print(f"\n📁 All files saved to organized folders in: {SAMPLE_DIR}")
        print("\n🎯 CSV Test Scenarios Covered:")
        print("   • Product price comparisons")
        print("   • Invoice validations")
        print("   • Edge cases (empty cells, special characters)")
        print("   • Decimal precision testing")
        print("   • Different delimiter support (comma, semicolon, tab)")
        print("   • Large dataset handling (1000 rows)")
        print("   • Vietnamese text support")
        print("   • Performance testing with large files")
        
    except Exception as e:
        print(f"❌ Error creating CSV files: {e}")