"""
Create comprehensive PDF test files for file comparison system self-testing
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Create sample directory
SAMPLE_DIR = "/Volumes/Workspace/1-SideProject/File_Diff/samples"
os.makedirs(SAMPLE_DIR, exist_ok=True)

def create_product_comparison_pdf1():
    """Create first product comparison PDF"""
    filename = os.path.join(SAMPLE_DIR, "product_comparison_v1.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    content = []
    
    # Title
    title = Paragraph("BÁO GIÁ SẢN PHẨM - PHIÊN BẢN 1.0", title_style)
    content.append(title)
    content.append(Spacer(12, 12))
    
    # Product table
    product_data = [
        ['STT', 'Mã SP', 'Tên sản phẩm', 'Đơn vị', 'Số lượng', 'Đơn giá', 'Thành tiền'],
        ['1', 'CC1500', 'Canxi Carbonate Coated Grade 1500T', 'kg', 1000, 75000, 75000000],
        ['2', 'CC800', 'Canxi Carbonate Uncoated Grade 800', 'kg', 2000, 45000, 90000000],
        ['3', 'TALC325', 'Bột Talc Mesh 325', 'kg', 500, 120000, 60000000],
        ['4', 'TALC600', 'Bột Talc Mesh 600', 'kg', 300, 180000, 54000000],
        ['5', 'KAOLIN', 'Kaolin Clay', 'kg', 800, 95000, 76000000],
        ['6', 'BENTONITE', 'Bentonite Sodium', 'kg', 400, 65000, 26000000],
    ]
    
    table = Table(product_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    content.append(table)
    content.append(Spacer(12, 24))
    
    # Summary
    summary_data = [
        ['Tổng cộng', '', '', '', '5000', '', '381000000'],
    ]
    
    summary_table = Table(summary_data, colWidths=[30*mm, 40*mm, 50*mm, 20*mm, 30*mm, 25*mm, 40*mm])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (4, 0), 'CENTER'),
        ('ALIGN', (5, 0), (-1, 0), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
    ]))
    
    content.append(summary_table)
    
    doc.build(content)
    return filename

def create_product_comparison_pdf2():
    """Create second product comparison PDF with differences"""
    filename = os.path.join(SAMPLE_DIR, "product_comparison_v2.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    content = []
    
    # Title
    title = Paragraph("BÁO GIÁ SẢN PHẨM - PHIÊN BẢN 2.0 (CẬP NHẬT)", title_style)
    content.append(title)
    content.append(Spacer(12, 12))
    
    # Product table with differences
    product_data = [
        ['STT', 'Mã SP', 'Tên sản phẩm', 'Đơn vị', 'Số lượng', 'Đơn giá', 'Thành tiền'],
        ['1', 'CC1500', 'Canxi Carbonate Coated Grade 1500T', 'kg', 1000, 78000, 78000000],  # Price changed
        ['2', 'CC800', 'Canxi Carbonate Uncoated Grade 800', 'kg', 2000, 45000, 90000000],  # Same
        ['3', 'TALC325', 'Bột Talc Mesh 325', 'kg', 550, 120000, 66000000],  # Quantity changed
        ['4', 'TALC600', 'Bột Talc Mesh 600', 'kg', 300, 185000, 55500000],  # Price changed
        ['5', 'KAOLIN', 'Kaolin Clay Premium', 'kg', 800, 95000, 76000000],  # Product name changed
        ['7', 'CALCITE', 'Canxi Calcite', 'kg', 200, 55000, 11000000],  # New product
    ]
    
    table = Table(product_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    content.append(table)
    content.append(Spacer(12, 24))
    
    # Summary
    summary_data = [
        ['Tổng cộng', '', '', '', '5350', '', '406500000'],
    ]
    
    summary_table = Table(summary_data, colWidths=[30*mm, 40*mm, 50*mm, 20*mm, 30*mm, 25*mm, 40*mm])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (4, 0), 'CENTER'),
        ('ALIGN', (5, 0), (-1, 0), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.red),
    ]))
    
    content.append(summary_table)
    
    doc.build(content)
    return filename

def create_invoice_pdf1():
    """Create first invoice PDF"""
    filename = os.path.join(SAMPLE_DIR, "invoice_001.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    content = []
    
    # Invoice header
    title = Paragraph("HÓA ĐƠN BÁN HÀNG #001", title_style)
    content.append(title)
    content.append(Spacer(12, 12))
    
    # Customer info
    customer_info = [
        ['Khách hàng:', 'Công ty TNHH XYZ'],
        ['Địa chỉ:', '123 Nguyễn Huệ, Q.1, TP.HCM'],
        ['Mã số thuế:', '0301234567'],
        ['Ngày:', '15/10/2025'],
    ]
    
    customer_table = Table(customer_info, colWidths=[60*mm, 80*mm])
    customer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    content.append(customer_table)
    content.append(Spacer(12, 24))
    
    # Invoice items
    invoice_data = [
        ['STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị', 'Số lượng', 'Đơn giá', 'Thành tiền'],
        ['1', 'Canxi Carbonate Coated 1500T', 'kg', 500, 75000, 37500000],
        ['2', 'Talc Powder 325 mesh', 'kg', 200, 120000, 24000000],
        ['3', 'Kaolin Clay', 'kg', 100, 95000, 9500000],
        ['4', 'Phí vận chuyển', 'lượt', 1, 500000, 500000],
    ]
    
    invoice_table = Table(invoice_data)
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    content.append(invoice_table)
    content.append(Spacer(12, 24))
    
    # Totals
    total_data = [
        ['Tạm tính:', '', '', '', '', '71500000'],
        ['VAT (10%):', '', '', '', '', '7150000'],
        ['Tổng cộng:', '', '', '', '', '78650000'],
    ]
    
    total_table = Table(total_data, colWidths=[100*mm, 20*mm, 20*mm, 20*mm, 20*mm, 40*mm])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (4, -1), 'RIGHT'),
        ('ALIGN', (5, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 2), (-1, -1), colors.red),
    ]))
    
    content.append(total_table)
    
    doc.build(content)
    return filename

def create_invoice_pdf2():
    """Create second invoice PDF with differences"""
    filename = os.path.join(SAMPLE_DIR, "invoice_002.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    content = []
    
    # Invoice header
    title = Paragraph("HÓA ĐƠN BÁN HÀNG #002 (ĐIỀU CHỈNH)", title_style)
    content.append(title)
    content.append(Spacer(12, 12))
    
    # Customer info
    customer_info = [
        ['Khách hàng:', 'Công ty TNHH XYZ'],
        ['Địa chỉ:', '123 Nguyễn Huệ, Q.1, TP.HCM'],
        ['Mã số thuế:', '0301234567'],
        ['Ngày:', '16/10/2025'],  # Date changed
    ]
    
    customer_table = Table(customer_info, colWidths=[60*mm, 80*mm])
    customer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    content.append(customer_table)
    content.append(Spacer(12, 24))
    
    # Invoice items with differences
    invoice_data = [
        ['STT', 'Tên hàng hóa, dịch vụ', 'Đơn vị', 'Số lượng', 'Đơn giá', 'Thành tiền'],
        ['1', 'Canxi Carbonate Coated 1500T', 'kg', 480, 75000, 36000000],  # Quantity changed
        ['2', 'Talc Powder 325 mesh', 'kg', 200, 125000, 25000000],  # Price changed
        ['3', 'Kaolin Clay Premium', 'kg', 100, 98000, 9800000],  # Product name and price changed
        ['4', 'Phí vận chuyển', 'lượt', 1, 450000, 450000],  # Shipping cost changed
        ['5', 'Chi phí đóng gói', 'cái', 10, 50000, 500000],  # New item
    ]
    
    invoice_table = Table(invoice_data)
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    content.append(invoice_table)
    content.append(Spacer(12, 24))
    
    # Totals
    total_data = [
        ['Tạm tính:', '', '', '', '', '71750000'],
        ['VAT (10%):', '', '', '', '', '7175000'],
        ['Tổng cộng:', '', '', '', '', '78925000'],
    ]
    
    total_table = Table(total_data, colWidths=[100*mm, 20*mm, 20*mm, 20*mm, 20*mm, 40*mm])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (4, -1), 'RIGHT'),
        ('ALIGN', (5, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 2), (-1, -1), colors.red),
    ]))
    
    content.append(total_table)
    
    doc.build(content)
    return filename

def create_multi_table_pdf():
    """Create PDF with multiple tables for complex testing"""
    filename = os.path.join(SAMPLE_DIR, "multi_table_data.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    content = []
    
    # Title
    title = Paragraph("BÁO CÁO KIỂM KÊ HÀNG TỒN KHO - NHIỀU BẢNG", title_style)
    content.append(title)
    content.append(Spacer(12, 12))
    
    # Table 1: Chemical Products
    subtitle1 = Paragraph("Bảng 1: Sản phẩm hóa chất", normal_style)
    content.append(subtitle1)
    content.append(Spacer(6, 6))
    
    chemical_data = [
        ['STT', 'Tên sản phẩm', 'Tồn đầu', 'Nhập về', 'Xuất bán', 'Tồn cuối'],
        ['1', 'Canxi Carbonate 1500T', 1000, 5000, 4500, 1500],
        ['2', 'Talc Powder 325', 500, 2000, 1800, 700],
        ['3', 'Kaolin Clay', 800, 3000, 2500, 1300],
    ]
    
    chemical_table = Table(chemical_data)
    chemical_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    
    content.append(chemical_table)
    content.append(Spacer(12, 12))
    
    # Table 2: Prices
    subtitle2 = Paragraph("Bảng 2: Bảng giá áp dụng", normal_style)
    content.append(subtitle2)
    content.append(Spacer(6, 6))
    
    price_data = [
        ['Sản phẩm', 'Đơn giá (VNĐ/kg)', 'Chiết khấu (%)', 'Giá thực tế'],
        ['Canxi Carbonate 1500T', '75,000', '5%', '71,250'],
        ['Talc Powder 325', '120,000', '3%', '116,400'],
        ['Kaolin Clay', '95,000', '7%', '88,350'],
    ]
    
    price_table = Table(price_data)
    price_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    
    content.append(price_table)
    content.append(Spacer(12, 12))
    
    # Table 3: Summary
    subtitle3 = Paragraph("Bảng 3: Tổng hợp giá trị tồn kho", normal_style)
    content.append(subtitle3)
    content.append(Spacer(6, 6))
    
    summary_data = [
        ['Sản phẩm', 'Số lượng tồn', 'Đơn giá', 'Thành tiền'],
        ['Canxi Carbonate 1500T', '1500', '71,250', '106,875,000'],
        ['Talc Powder 325', '700', '116,400', '81,480,000'],
        ['Kaolin Clay', '1300', '88,350', '114,855,000'],
        ['Tổng cộng', '3500', '-', '303,210,000'],
    ]
    
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightyellow),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (3, 3), (3, 3), 'Helvetica-Bold'),
        ('TEXTCOLOR', (3, 3), (3, 3), colors.red),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    
    content.append(summary_table)
    
    doc.build(content)
    return filename

def create_edge_case_pdf():
    """Create PDF with edge cases (empty cells, special characters, etc.)"""
    filename = os.path.join(SAMPLE_DIR, "edge_cases_test.pdf")
    doc = SimpleDocTemplate(filename, pagesize=A4)
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    content = []
    
    # Title
    title = Paragraph("TEST CASES: DỮ LIỆU ĐẶC BIỆT", title_style)
    content.append(title)
    content.append(Spacer(12, 12))
    
    # Table with edge cases
    edge_data = [
        ['STT', 'Tên SP', 'Mô tả', 'Số lượng', 'Đơn giá', 'Thành tiền', 'Ghi chú'],
        ['1', 'SP001', 'Sản phẩm thường', 100, 50000, 5000000, 'Bình thường'],
        ['2', 'SP002', '', 50, '', '', 'Giá chưa xác định'],  # Empty cells
        ['3', 'SP003', 'Sản phẩm đặc biệt (ký tự: @#$%^&*)', None, None, None, 'Đặc biệt'],  # Special chars and None
        ['4', '', 'Sản phẩm không có mã', 25, 75000, 1875000, ''],  # Empty product name
        ['5', 'SP005', 'Sản phẩm với số âm (trả hàng)', -10, 100000, -1000000, 'Trả hàng'],  # Negative number
        ['6', 'SP006', 'Sản phẩm với số thập phân', 5.5, 33333.33, 183333.32, 'Số lẻ'],
        ['7', 'SP007', 'Sản phẩm dài quá... ' * 10, 1000, 999999, 999999000, 'Tên rất dài'],  # Long text
        ['8', 'SP008', 'Sản phẩm có dấu: Nguyễn Văn A', 1, 1000000, 1000000, 'Có dấu tiếng Việt'],  # Vietnamese
    ]
    
    edge_table = Table(edge_data)
    edge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),  # Description column left-aligned
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Smaller font for more content
        ('WORDWRAP', (0, 0), (-1, -1), 'LTR'),
    ]))
    
    content.append(edge_table)
    
    doc.build(content)
    return filename

# Create all test files
if __name__ == "__main__":
    print("Creating PDF test files for comprehensive self-testing...")
    
    files_created = []
    
    try:
        # Product comparison files
        files_created.append(create_product_comparison_pdf1())
        files_created.append(create_product_comparison_pdf2())
        
        # Invoice files
        files_created.append(create_invoice_pdf1())
        files_created.append(create_invoice_pdf2())
        
        # Multi-table file
        files_created.append(create_multi_table_pdf())
        
        # Edge cases file
        files_created.append(create_edge_case_pdf())
        
        print(f"\n✅ Successfully created {len(files_created)} PDF test files:")
        for file in files_created:
            print(f"   📄 {os.path.basename(file)}")
        
        print(f"\n📁 All files saved to: {SAMPLE_DIR}")
        print("\n🎯 Test Scenarios Covered:")
        print("   • Product price comparisons")
        print("   • Invoice validations")
        print("   • Multi-table extraction")
        print("   • Edge cases (empty cells, special characters)")
        print("   • Vietnamese text support")
        print("   • Decimal numbers and calculations")
        print("   • Long text handling")
        
    except Exception as e:
        print(f"❌ Error creating PDF files: {e}")