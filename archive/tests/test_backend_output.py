#!/usr/bin/env python3
"""
Simple script to test backend output
"""

import sys
import os
import asyncio

# Add backend directory to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

print("🚀 Testing Backend Output")
print("=" * 50)

async def main():
    try:
        # Test imports
        print("📦 Testing imports...")
        from app.config import get_settings
        from app.models import APIError, HealthResponse
        from app.main import app
        print("   ✅ All imports successful")
        
        # Test settings
        print("\n⚙️  Testing settings...")
        settings = get_settings()
        print(f"   - App Name: {settings.app_name}")
        print(f"   - Version: {settings.app_version}")
        print(f"   - Debug: {settings.debug}")
        print(f"   - Upload Dir: {settings.upload_dir}")
        
        # Test FastAPI app
        print("\n🌐 Testing FastAPI app...")
        print(f"   - App Title: {app.title}")
        print(f"   - App Version: {app.version}")
        print(f"   - Debug Mode: {app.debug}")
        
        # Test routes
        print("\n🛣️  Available routes:")
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                methods = list(route.methods) if route.methods else []
                print(f"   - {route.path}: {', '.join(methods)}")
        
        # Test processors
        print("\n📄 Testing processors...")
        from processors.csv_processor import CSVProcessor
        from processors.excel_processor import ExcelProcessor
        from processors.pdf_processor import PDFProcessor
        
        csv_proc = CSVProcessor()
        excel_proc = ExcelProcessor()
        pdf_proc = PDFProcessor()
        
        print(f"   - CSV Processor: {type(csv_proc).__name__}")
        print(f"   - Excel Processor: {type(excel_proc).__name__}")
        print(f"   - PDF Processor: {type(pdf_proc).__name__}")
        
        # Test comparator
        print("\n🔍 Testing comparator...")
        from comparators.data_comparator import DataComparator
        comparator = DataComparator()
        print(f"   - Data Comparator: {type(comparator).__name__}")
        
        # Test logging
        print("\n📝 Testing logging system...")
        from utils.logger import get_process_logger
        logger = get_process_logger('test')
        
        # Test file processing
        print("\n🧪 Testing file processing...")
        test_file = 'samples/test_file1.csv'
        if os.path.exists(test_file):
            result = await csv_proc.process(test_file)
            print(f"   - CSV Processing: ✅ {len(result.get('structured_data', []))} tables")
            print(f"   - Processing time: {result.get('metadata', {}).get('processing_time', 0):.3f}s")
        else:
            print(f"   - CSV Processing: ⚠️  Test file not found: {test_file}")
        
        # Test Excel processing
        test_excel = 'samples/test_file1.xlsx'
        if os.path.exists(test_excel):
            result = await excel_proc.process(test_excel)
            print(f"   - Excel Processing: ✅ {len(result.get('structured_data', []))} tables")
            print(f"   - Processing time: {result.get('metadata', {}).get('processing_time', 0):.3f}s")
        else:
            print(f"   - Excel Processing: ⚠️  Test file not found: {test_excel}")
        
        print("\n🎉 All backend tests completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   Please ensure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())