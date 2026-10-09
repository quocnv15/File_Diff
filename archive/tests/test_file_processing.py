#!/usr/bin/env python3
"""
Simple test for new sample files - focusing on file processing
"""

import os
import sys
import asyncio
import time
from pathlib import Path

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from backend.processors.csv_processor import CSVProcessor
from backend.processors.excel_processor import ExcelProcessor
from backend.processors.pdf_processor import PDFProcessor

class SimpleFileTestRunner:
    """Simple test runner focusing on file processing"""
    
    def __init__(self):
        self.samples_dir = Path(__file__).parent / 'samples'
        self.processors = {
            'csv': CSVProcessor(),
            'xlsx': ExcelProcessor(),
            'xls': ExcelProcessor(),
            'pdf': PDFProcessor()
        }
        self.results = []
    
    async def test_file(self, file_path: Path):
        """Test single file processing"""
        if not file_path.exists():
            return {
                'file': file_path.name,
                'success': False,
                'error': 'File not found'
            }
        
        file_ext = file_path.suffix.lower().lstrip('.')
        if file_ext not in self.processors:
            return {
                'file': file_path.name,
                'success': False,
                'error': f'Unsupported format: {file_ext}'
            }
        
        processor = self.processors[file_ext]
        
        try:
            start_time = time.time()
            result = await processor.process(str(file_path))
            processing_time = time.time() - start_time
            
            # Check if processing was successful
            success = result and 'structured_data' in result and len(result['structured_data']) > 0
            
            return {
                'file': file_path.name,
                'success': success,
                'processing_time': processing_time,
                'structured_data_count': len(result.get('structured_data', [])),
                'has_markdown': bool(result.get('markdown_content')),
                'file_size': file_path.stat().st_size,
                'error': None if success else 'No structured data extracted'
            }
        except Exception as e:
            return {
                'file': file_path.name,
                'success': False,
                'error': str(e),
                'file_size': file_path.stat().st_size if file_path.exists() else 0
            }
    
    async def run_organized_tests(self):
        """Run tests on organized sample files"""
        print("🧪 Testing Organized Sample Files")
        print("=" * 50)
        
        test_dirs = [
            ('product_comparisons', 'Product Comparisons'),
            ('invoice_comparisons', 'Invoice Comparisons'),
            ('multi_table_tests', 'Multi-Table Tests'),
            ('edge_cases', 'Edge Cases'),
            ('decimal_tests', 'Decimal Tests')
        ]
        
        for dir_name, description in test_dirs:
            print(f"\n📁 {description}")
            print("-" * len(description))
            
            test_dir = self.samples_dir / dir_name
            if not test_dir.exists():
                print(f"   ❌ Directory not found: {test_dir}")
                continue
            
            # Get all files in directory
            files = list(test_dir.glob('*'))
            files = [f for f in files if f.is_file() and f.suffix.lower() in ['.csv', '.xlsx', '.xls', '.pdf']]
            
            if not files:
                print(f"   ⚠️  No test files found")
                continue
            
            for file_path in sorted(files):
                result = await self.test_file(file_path)
                self.results.append(result)
                
                if result['success']:
                    print(f"   ✅ {result['file']} ({result['processing_time']:.3f}s, {result['structured_data_count']} tables)")
                else:
                    print(f"   ❌ {result['file']} - {result['error']}")
    
    async def run_original_tests(self):
        """Run tests on original sample files"""
        print(f"\n📁 Original Sample Files")
        print("-" * 25)
        
        original_files = [
            'test_file1.csv',
            'test_file2.csv',
            'test_file1.xlsx',
            'test_file2.xlsx',
            '31JOC.pdf',
            '31JOC.xlsx'
        ]
        
        for filename in original_files:
            file_path = self.samples_dir / filename
            result = await self.test_file(file_path)
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['file']} ({result['processing_time']:.3f}s, {result['structured_data_count']} tables)")
            else:
                print(f"   ❌ {result['file']} - {result['error']}")
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"📊 SIMPLE FILE PROCESSING TEST SUMMARY")
        print(f"{'='*60}")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Files Tested: {total_tests}")
        print(f"Successfully Processed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests / total_tests * 100):.1f}%")
        
        if passed_tests > 0:
            avg_time = sum(r['processing_time'] for r in self.results if r['success']) / passed_tests
            total_data = sum(r['structured_data_count'] for r in self.results if r['success'])
            print(f"Average Processing Time: {avg_time:.3f}s")
            print(f"Total Tables Extracted: {total_data}")
        
        # Group by file type
        print(f"\n📊 Results by File Type:")
        file_types = {}
        for result in self.results:
            file_ext = result['file'].split('.')[-1].lower()
            if file_ext not in file_types:
                file_types[file_ext] = {'passed': 0, 'failed': 0, 'total_time': 0, 'total_tables': 0}
            
            if result['success']:
                file_types[file_ext]['passed'] += 1
                file_types[file_ext]['total_time'] += result['processing_time']
                file_types[file_ext]['total_tables'] += result['structured_data_count']
            else:
                file_types[file_ext]['failed'] += 1
        
        for file_ext, stats in file_types.items():
            total = stats['passed'] + stats['failed']
            success_rate = (stats['passed'] / total * 100) if total > 0 else 0
            avg_time = stats['total_time'] / stats['passed'] if stats['passed'] > 0 else 0
            
            print(f"   - {file_ext.upper()}: {stats['passed']}/{total} ({success_rate:.1f}%)")
            if stats['passed'] > 0:
                print(f"     Avg time: {avg_time:.3f}s, Tables: {stats['total_tables']}")
        
        if failed_tests == 0:
            print(f"\n🎉 ALL FILES PROCESSED SUCCESSFULLY!")
        elif passed_tests / total_tests >= 0.8:
            print(f"\n✅ GOOD PERFORMANCE! Most files processed successfully.")
        else:
            print(f"\n⚠️  Some processing issues detected.")
        
        print(f"{'='*60}")
    
    async def run_all_tests(self):
        """Run all file processing tests"""
        print("🚀 Starting Simple File Processing Tests")
        print(f"Testing files from: {self.samples_dir}")
        
        start_time = time.time()
        
        await self.run_organized_tests()
        await self.run_original_tests()
        
        total_time = time.time() - start_time
        print(f"\n⏱️  Total test execution time: {total_time:.2f} seconds")
        self.print_summary()

async def main():
    """Main function"""
    runner = SimpleFileTestRunner()
    await runner.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())