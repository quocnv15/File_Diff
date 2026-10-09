"""
Create comprehensive Excel test files for file comparison system self-testing
"""

import os
import pandas as pd
from datetime import datetime, timedelta
import random

# Create sample directory
SAMPLE_DIR = "/Volumes/Workspace/1-SideProject/File_Diff/samples"

def create_product_comparison_excel():
    """Create Excel file with product comparison data"""
    
    # Version 1 data
    products_v1 = [
        {
            'STT': 1,
            'Mã SP': 'CC1500',
            'Tên sản phẩm': 'Canxi Carbonate Coated Grade 1500T',
            'Đơn vị': 'kg',
            'Số lượng': 1000,
            'Đơn giá': 75000,
            'Thành tiền': 75000000
        },
        {
            'STT': 2,
            'Mã SP': 'CC800',
            'Tên sản phẩm': 'Canxi Carbonate Uncoated Grade 800',
            'Đơn vị': 'kg',
            'Số lượng': 2000,
            'Đơn giá': 45000,
            'Thành tiền': 90000000
        },
        {
            'STT': 3,
            'Mã SP': 'TALC325',
            'Tên sản phẩm': 'Bột Talc Mesh 325',
            'Đơn vị': 'kg',
            'Số lượng': 500,
            'Đơn giá': 120000,
            'Thành tiền': 60000000
        },
        {
            'STT': 4,
            'Mã SP': 'TALC600',
            'Tên sản phẩm': 'Bột Talc Mesh 600',
            'Đơn vị': 'kg',
            'Số lượng': 300,
            'Đơn giá': 180000,
            'Thành tiền': 54000000
        },
        {
            'STT': 5,
            'Mã SP': 'KAOLIN',
            'Tên sản phẩm': 'Kaolin Clay',
            'Đơn vị': 'kg',
            'Số lượng': 800,
            'Đơn giá': 95000,
            'Thành tiền': 76000000
        }
    ]
    
    df_v1 = pd.DataFrame(products_v1)
    filename_v1 = os.path.join(SAMPLE_DIR, "product_comparison_v1.xlsx")
    df_v1.to_excel(filename_v1, index=False, sheet_name='Báo giá v1')
    
    # Version 2 data with differences
    products_v2 = [
        {
            'STT': 1,
            'Mã SP': 'CC1500',
            'Tên sản phẩm': 'Canxi Carbonate Coated Grade 1500T',
            'Đơn vị': 'kg',
            'Số lượng': 1000,
            'Đơn giá': 78000,  # Price changed
            'Thành tiền': 78000000
        },
        {
            'STT': 2,
            'Mã SP': 'CC800',
            'Tên sản phẩm': 'Canxi Carbonate Uncoated Grade 800',
            'Đơn vị': 'kg',
            'Số lượng': 2000,
            'Đơn giá': 45000,
            'Thành tiền': 90000000
        },
        {
            'STT': 3,
            'Mã SP': 'TALC325',
            'Tên sản phẩm': 'Bột Talc Mesh 325',
            'Đơn vị': 'kg',
            'Số lượng': 550,  # Quantity changed
            'Đơn giá': 120000,
            'Thành tiền': 66000000
        },
        {
            'STT': 4,
            'Mã SP': 'TALC600',
            'Tên sản phẩm': 'Bột Talc Mesh 600 Premium',  # Name changed
            'Đơn vị': 'kg',
            'Số lượng': 300,
            'Đơn giá': 185000,  # Price changed
            'Thành tiền': 55500000
        },
        {
            'STT': 6,
            'Mã SP': 'CALCITE',  # New product
            'Tên sản phẩm': 'Canxi Calcite',
            'Đơn vị': 'kg',
            'Số lượng': 200,
            'Đơn giá': 55000,
            'Thành tiền': 11000000
        }
    ]
    
    df_v2 = pd.DataFrame(products_v2)
    filename_v2 = os.path.join(SAMPLE_DIR, "product_comparison_v2.xlsx")
    
    with pd.ExcelWriter(filename_v2, engine='openpyxl') as writer:
        df_v2.to_excel(writer, sheet_name='Báo giá v2', index=False)
        
        # Add summary sheet
        summary_data = {
            'Thông tin': ['Tổng sản phẩm', 'Tổng số lượng', 'Tổng giá trị'],
            'Phiên bản 1': [5, 4600, 355000000],
            'Phiên bản 2': [5, 4650, 360500000],
            'Chênh lệch': [0, 50, 5500000]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Tổng hợp', index=False)
    
    return filename_v1, filename_v2

def create_invoice_excel():
    """Create Excel file with invoice data"""
    
    # Invoice 1
    invoice1_items = [
        {
            'STT': 1,
            'Tên hàng hóa, dịch vụ': 'Canxi Carbonate Coated 1500T',
            'Đơn vị': 'kg',
            'Số lượng': 500,
            'Đơn giá': 75000,
            'Thành tiền': 37500000
        },
        {
            'STT': 2,
            'Tên hàng hóa, dịch vụ': 'Talc Powder 325 mesh',
            'Đơn vị': 'kg',
            'Số lượng': 200,
            'Đơn giá': 120000,
            'Thành tiền': 24000000
        },
        {
            'STT': 3,
            'Tên hàng hóa, dịch vụ': 'Kaolin Clay',
            'Đơn vị': 'kg',
            'Số lượng': 100,
            'Đơn giá': 95000,
            'Thành tiền': 9500000
        },
        {
            'STT': 4,
            'Tên hàng hóa, dịch vụ': 'Phí vận chuyển',
            'Đơn vị': 'lượt',
            'Số lượng': 1,
            'Đơn giá': 500000,
            'Thành tiền': 500000
        }
    ]
    
    df_invoice1 = pd.DataFrame(invoice1_items)
    filename_invoice1 = os.path.join(SAMPLE_DIR, "invoice_001.xlsx")
    
    with pd.ExcelWriter(filename_invoice1, engine='openpyxl') as writer:
        # Customer info sheet
        customer_info = pd.DataFrame([
            ['Khách hàng', 'Công ty TNHH XYZ'],
            ['Địa chỉ', '123 Nguyễn Huệ, Q.1, TP.HCM'],
            ['Mã số thuế', '0301234567'],
            ['Ngày', '15/10/2025'],
            ['Số hóa đơn', 'HD001']
        ], columns=['Thông tin', 'Giá trị'])
        customer_info.to_excel(writer, sheet_name='Thông tin KH', index=False)
        
        # Invoice items
        df_invoice1.to_excel(writer, sheet_name='Chi tiết hóa đơn', index=False)
        
        # Totals
        totals = pd.DataFrame([
            ['Tạm tính', 71500000],
            ['VAT (10%)', 7150000],
            ['Tổng cộng', 78650000]
        ], columns=['Loại', 'Số tiền'])
        totals.to_excel(writer, sheet_name='Tổng cộng', index=False)
    
    # Invoice 2 with differences
    invoice2_items = [
        {
            'STT': 1,
            'Tên hàng hóa, dịch vụ': 'Canxi Carbonate Coated 1500T',
            'Đơn vị': 'kg',
            'Số lượng': 480,  # Quantity changed
            'Đơn giá': 75000,
            'Thành tiền': 36000000
        },
        {
            'STT': 2,
            'Tên hàng hóa, dịch vụ': 'Talc Powder 325 mesh',
            'Đơn vị': 'kg',
            'Số lượng': 200,
            'Đơn giá': 125000,  # Price changed
            'Thành tiền': 25000000
        },
        {
            'STT': 3,
            'Tên hàng hóa, dịch vụ': 'Kaolin Clay Premium',  # Name changed
            'Đơn vị': 'kg',
            'Số lượng': 100,
            'Đơn giá': 98000,  # Price changed
            'Thành tiền': 9800000
        },
        {
            'STT': 4,
            'Tên hàng hóa, dịch vụ': 'Phí vận chuyển',
            'Đơn vị': 'lượt',
            'Số lượng': 1,
            'Đơn giá': 450000,  # Price changed
            'Thành tiền': 450000
        },
        {
            'STT': 5,
            'Tên hàng hóa, dịch vụ': 'Chi phí đóng gói',  # New item
            'Đơn vị': 'cái',
            'Số lượng': 10,
            'Đơn giá': 50000,
            'Thành tiền': 500000
        }
    ]
    
    df_invoice2 = pd.DataFrame(invoice2_items)
    filename_invoice2 = os.path.join(SAMPLE_DIR, "invoice_002.xlsx")
    
    with pd.ExcelWriter(filename_invoice2, engine='openpyxl') as writer:
        # Customer info sheet
        customer_info2 = pd.DataFrame([
            ['Khách hàng', 'Công ty TNHH XYZ'],
            ['Địa chỉ', '123 Nguyễn Huệ, Q.1, TP.HCM'],
            ['Mã số thuế', '0301234567'],
            ['Ngày', '16/10/2025'],  # Date changed
            ['Số hóa đơn', 'HD002']  # Invoice number changed
        ], columns=['Thông tin', 'Giá trị'])
        customer_info2.to_excel(writer, sheet_name='Thông tin KH', index=False)
        
        # Invoice items
        df_invoice2.to_excel(writer, sheet_name='Chi tiết hóa đơn', index=False)
        
        # Totals
        totals2 = pd.DataFrame([
            ['Tạm tính', 71750000],
            ['VAT (10%)', 7175000],
            ['Tổng cộng', 78925000]
        ], columns=['Loại', 'Số tiền'])
        totals2.to_excel(writer, sheet_name='Tổng cộng', index=False)
    
    return filename_invoice1, filename_invoice2

def create_multi_sheet_excel():
    """Create Excel file with multiple sheets for complex testing"""
    filename = os.path.join(SAMPLE_DIR, "multi_sheet_data.xlsx")
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Sheet 1: Inventory
        inventory_data = [
            ['Mã SP', 'Tên sản phẩm', 'Tồn đầu kỳ', 'Nhập về', 'Xuất bán', 'Tồn cuối kỳ'],
            ['CC1500', 'Canxi Carbonate 1500T', 1000, 5000, 4500, 1500],
            ['TALC325', 'Talc Powder 325', 500, 2000, 1800, 700],
            ['KAOLIN', 'Kaolin Clay', 800, 3000, 2500, 1300],
            ['TALC600', 'Talc Powder 600', 300, 1000, 800, 500]
        ]
        df_inventory = pd.DataFrame(inventory_data[1:], columns=inventory_data[0])
        df_inventory.to_excel(writer, sheet_name='Tồn kho', index=False)
        
        # Sheet 2: Prices
        price_data = [
            ['Mã SP', 'Tên sản phẩm', 'Đơn giá cơ bản', 'Chiết khấu (%)', 'Giá bán'],
            ['CC1500', 'Canxi Carbonate 1500T', 75000, 5, 71250],
            ['TALC325', 'Talc Powder 325', 120000, 3, 116400],
            ['KAOLIN', 'Kaolin Clay', 95000, 7, 88350],
            ['TALC600', 'Talc Powder 600', 180000, 10, 162000]
        ]
        df_prices = pd.DataFrame(price_data[1:], columns=price_data[0])
        df_prices.to_excel(writer, sheet_name='Bảng giá', index=False)
        
        # Sheet 3: Customers
        customer_data = [
            ['Mã KH', 'Tên khách hàng', 'Địa chỉ', 'SĐT', 'Loại KH'],
            ['KH001', 'Công ty ABC', 'Q1, TP.HCM', '0901234567', 'VIP'],
            ['KH002', 'Công ty XYZ', 'Q7, TP.HCM', '0909876543', 'Thường'],
            ['KH003', 'Công ty DEF', 'Bình Thạnh', '0901112222', 'VIP']
        ]
        df_customers = pd.DataFrame(customer_data[1:], columns=customer_data[0])
        df_customers.to_excel(writer, sheet_name='Khách hàng', index=False)
        
        # Sheet 4: Summary
        summary_data = [
            ['Báo cáo', 'Giá trị'],
            ['Tổng sản phẩm', 4],
            ['Tổng tồn kho', 4000],
            ['Giá trị tồn kho', 236300000],
            ['Số khách hàng', 3],
            ['Tỷ lệ khách VIP', '66.67%']
        ]
        df_summary = pd.DataFrame(summary_data[1:], columns=summary_data[0])
        df_summary.to_excel(writer, sheet_name='Tổng hợp', index=False)
    
    return filename

def create_edge_cases_excel():
    """Create Excel file with edge cases"""
    filename = os.path.join(SAMPLE_DIR, "edge_cases_excel.xlsx")
    
    edge_data = [
        {
            'STT': 1,
            'Mã SP': 'SP001',
            'Tên sản phẩm': 'Sản phẩm bình thường',
            'Mô tả': 'Mô tả đầy đủ',
            'Số lượng': 100,
            'Đơn giá': 50000,
            'Thành tiền': 5000000,
            'Ghi chú': 'Bình thường'
        },
        {
            'STT': 2,
            'Mã SP': 'SP002',
            'Tên sản phẩm': 'Sản phẩm thiếu thông tin',
            'Mô tả': None,  # None value
            'Số lượng': '',  # Empty string
            'Đơn giá': None,  # None value
            'Thành tiền': '',  # Empty string
            'Ghi chú': 'Thiếu dữ liệu'
        },
        {
            'STT': 3,
            'Mã SP': 'SP003',
            'Tên sản phẩm': 'Sản phẩm ký tự đặc biệt !@#$%^&*()',
            'Mô tả': 'Mô tả có dấu: Nguyễn Văn A - Đỗ Thị B',
            'Số lượng': 5.5,  # Decimal number
            'Đơn giá': 33333.333,  # Decimal price
            'Thành tiền': 183333.33,  # Decimal total
            'Ghi chú': 'Số thập phân'
        },
        {
            'STT': 4,
            'Mã SP': '',  # Empty code
            'Tên sản phẩm': None,  # None name
            'Mô tả': 'Sản phẩm không có mã và tên',
            'Số lượng': -10,  # Negative number (trả hàng)
            'Đơn giá': 100000,
            'Thành tiền': -1000000,
            'Ghi chú': 'Trả hàng'
        },
        {
            'STT': 5,
            'Mã SP': 'SP005',
            'Tên sản phẩm': 'Sản phẩm với số 0',
            'Mô tả': 'Kiểm tra giá trị 0',
            'Số lượng': 0,
            'Đơn giá': 0,
            'Thành tiền': 0,
            'Ghi chú': 'Giá trị bằng 0'
        },
        {
            'STT': 6,
            'Mã SP': 'SP006',
            'Tên sản phẩm': 'Sản phẩm có số rất lớn',
            'Mô tả': 'Số lượng lớn để kiểm tra định dạng',
            'Số lượng': 999999,
            'Đơn giá': 999999999,
            'Thành tiền': 999999000001,
            'Ghi chú': 'Số lớn'
        }
    ]
    
    df_edge = pd.DataFrame(edge_data)
    df_edge.to_excel(filename, index=False, sheet_name='Edge Cases')
    
    return filename

def create_decimal_precision_excel():
    """Create Excel file to test decimal precision"""
    filename = os.path.join(SAMPLE_DIR, "decimal_precision_test.xlsx")
    
    decimal_data = [
        {
            'STT': 1,
            'Tên sản phẩm': 'Sản phẩm A',
            'Số lượng': 1.123456789,
            'Đơn giá': 12345.6789,
            'Thành tiền': 13873.4457,
            'VAT 10%': 1387.34457,
            'Tổng cộng': 15260.79027
        },
        {
            'STT': 2,
            'Tên sản phẩm': 'Sản phẩm B',
            'Số lượng': 2.5,
            'Đơn giá': 9999.99,
            'Thành tiền': 24999.975,
            'VAT 10%': 2499.9975,
            'Tổng cộng': 27499.9725
        },
        {
            'STT': 3,
            'Tên sản phẩm': 'Sản phẩm C',
            'Số lượng': 0.333333,
            'Đơn giá': 30000,
            'Thành tiền': 9999.99,
            'VAT 10%': 999.999,
            'Tổng cộng': 10999.989
        }
    ]
    
    df_decimal = pd.DataFrame(decimal_data)
    df_decimal.to_excel(filename, index=False, sheet_name='Decimal Precision')
    
    return filename

# Create all Excel test files
if __name__ == "__main__":
    print("Creating Excel test files for comprehensive self-testing...")
    
    files_created = []
    
    try:
        # Product comparison files
        prod1, prod2 = create_product_comparison_excel()
        files_created.extend([prod1, prod2])
        
        # Invoice files
        inv1, inv2 = create_invoice_excel()
        files_created.extend([inv1, inv2])
        
        # Multi-sheet file
        files_created.append(create_multi_sheet_excel())
        
        # Edge cases file
        files_created.append(create_edge_cases_excel())
        
        # Decimal precision file
        files_created.append(create_decimal_precision_excel())
        
        print(f"\n✅ Successfully created {len(files_created)} Excel test files:")
        for file in files_created:
            print(f"   📊 {os.path.basename(file)}")
        
        print(f"\n📁 All files saved to: {SAMPLE_DIR}")
        print("\n🎯 Excel Test Scenarios Covered:")
        print("   • Product price comparisons")
        print("   • Invoice validations")
        print("   • Multi-sheet processing")
        print("   • Edge cases (empty cells, None values, negative numbers)")
        print("   • Decimal precision testing")
        print("   • Large number handling")
        print("   • Vietnamese text support")
        print("   • Special characters handling")
        
    except Exception as e:
        print(f"❌ Error creating Excel files: {e}")