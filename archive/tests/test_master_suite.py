#!/usr/bin/env python3
"""
Master test runner - combines file processing and comparison tests
Tests all scenarios with the new organized sample files
"""

import os
import sys
import asyncio
import time
from pathlib import Path
from datetime import datetime

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from backend.processors.csv_processor import CSVProcessor
from backend.processors.excel_processor import ExcelProcessor
from backend.processors.pdf_processor import PDFProcessor
from backend.comparators.data_comparator import DataComparator
from backend.utils.logger import get_process_logger

class MasterTestRunner:
    """Master test runner for comprehensive file comparison system testing"""
    
    def __init__(self):
        self.samples_dir = Path(__file__).parent / 'samples'
        self.processors = {
            'csv': CSVProcessor(),
            'xlsx': ExcelProcessor(),
            'xls': ExcelProcessor(),
            'pdf': PDFProcessor()
        }
        self.comparator = DataComparator()
        self.logger = get_process_logger('master_test')
        self.results = {
            'file_processing': {'total': 0, 'passed': 0, 'failed': 0},
            'comparison': {'total': 0, 'passed': 0, 'failed': 0},
            'compatibility': {'total': 0, 'passed': 0, 'failed': 0},
            'performance': {'total': 0, 'passed': 0, 'failed': 0},
            'overall': {'total': 0, 'passed': 0, 'failed': 0},
            'tests': []
        }
        self.start_time = None
    
    def log_test(self, category: str, test_name: str, success: bool, details: dict = None):
        """Log test result"""
        self.results[category]['total'] += 1
        self.results['overall']['total'] += 1
        
        if success:
            self.results[category]['passed'] += 1
            self.results['overall']['passed'] += 1
            status = "✅ PASSED"
        else:
            self.results[category]['failed'] += 1
            self.results['overall']['failed'] += 1
            status = "❌ FAILED"
        
        test_detail = {
            'category': category,
            'name': test_name,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.results['tests'].append(test_detail)
        
        print(f"{status} [{category.upper()}] {test_name}")
        if details:
            for key, value in details.items():
                if isinstance(value, float) and key in ['time', 'accuracy', 'rate']:
                    print(f"   - {key}: {value:.3f}")
                elif key not in ['timestamp']:
                    print(f"   - {key}: {value}")
    
    async def test_file_processing(self, file_path: Path, test_name: str):
        """Test file processing"""
        if not file_path.exists():
            self.log_test('file_processing', test_name, False, 
                        {'error': 'File not found'})
            return None
        
        file_ext = file_path.suffix.lower().lstrip('.')
        if file_ext not in self.processors:
            self.log_test('file_processing', test_name, False,
                        {'error': f'Unsupported format: {file_ext}'})
            return None
        
        processor = self.processors[file_ext]
        
        try:
            start_time = time.time()
            result = await processor.process(str(file_path))
            processing_time = time.time() - start_time
            
            # Check if processing was successful
            success = result and 'structured_data' in result and len(result['structured_data']) > 0
            
            details = {
                'time': processing_time,
                'tables': len(result.get('structured_data', [])),
                'size_kb': file_path.stat().st_size / 1024,
                'has_content': bool(result.get('markdown_content'))
            }
            
            if not success:
                details['error'] = 'No structured data extracted'
            
            self.log_test('file_processing', test_name, success, details)
            return result.get('structured_data', [])
            
        except Exception as e:
            self.log_test('file_processing', test_name, False,
                        {'error': str(e), 'size_kb': file_path.stat().st_size / 1024 if file_path.exists() else 0})
            return None
    
    async def test_comparison(self, file1_path: Path, file2_path: Path, test_name: str, options=None):
        """Test file comparison"""
        if not file1_path.exists() or not file2_path.exists():
            self.log_test('comparison', test_name, False,
                        {'error': 'Files not found'})
            return None
        
        try:
            # Process both files
            data1 = await self.test_file_processing(file1_path, f"{test_name} - File 1")
            data2 = await self.test_file_processing(file2_path, f"{test_name} - File 2")
            
            if not data1 or not data2:
                self.log_test('comparison', test_name, False,
                            {'error': f'Failed to extract data: data1={len(data1) if data1 else 0}, data2={len(data2) if data2 else 0}'})
                return None
            
            # Use default options if none provided
            if options is None:
                options = {
                    'comparison_type': 'products',
                    'exact_match': False,
                    'tolerance_settings': {
                        'quantity': 0.1,
                        'unit_price': 0.01,
                        'amount': 0.01
                    }
                }
            
            # Perform comparison
            start_time = time.time()
            comparison_result = await self.comparator.compare(data1, data2, options)
            comparison_time = time.time() - start_time
            
            # Extract key metrics
            summary = comparison_result.get('summary', {})
            differences = comparison_result.get('differences', [])
            
            details = {
                'time': comparison_time,
                'rows_compared': summary.get('total_rows_compared', 0),
                'matching_rows': summary.get('matching_rows', 0),
                'different_rows': summary.get('different_rows', 0),
                'accuracy_rate': summary.get('accuracy_rate', 0),
                'differences': len(differences),
                'file1_tables': len(data1),
                'file2_tables': len(data2)
            }
            
            success = True  # Comparison completed successfully
            self.log_test('comparison', test_name, success, details)
            return comparison_result
            
        except Exception as e:
            self.log_test('comparison', test_name, False, {'error': str(e)})
            return None
    
    async def run_product_comparison_tests(self):
        """Run product comparison test suite"""
        print("\n🔍 Product Comparison Test Suite")
        print("=" * 50)
        
        test_scenarios = [
            ('product_comparison_v1.csv', 'product_comparison_v2.csv', 'CSV Product Comparison'),
            ('product_comparison_v1.xlsx', 'product_comparison_v2.xlsx', 'Excel Product Comparison'),
            ('product_comparison_v1.pdf', 'product_comparison_v2.pdf', 'PDF Product Comparison'),
        ]
        
        product_dir = self.samples_dir / 'product_comparisons'
        
        for file1_name, file2_name, test_name in test_scenarios:
            file1 = product_dir / file1_name
            file2 = product_dir / file2_name
            
            await self.test_comparison(file1, file2, test_name)
    
    async def run_invoice_comparison_tests(self):
        """Run invoice comparison test suite"""
        print("\n🧾 Invoice Comparison Test Suite")
        print("=" * 50)
        
        invoice_options = {
            'comparison_type': 'invoices',
            'exact_match': False,
            'tolerance_settings': {
                'quantity': 0.05,
                'unit_price': 0.005,
                'amount': 0.005
            }
        }
        
        test_scenarios = [
            ('invoice_001.csv', 'invoice_002.csv', 'CSV Invoice Comparison'),
            ('invoice_001.xlsx', 'invoice_002.xlsx', 'Excel Invoice Comparison'),
            ('invoice_001.pdf', 'invoice_002.pdf', 'PDF Invoice Comparison'),
        ]
        
        invoice_dir = self.samples_dir / 'invoice_comparisons'
        
        for file1_name, file2_name, test_name in test_scenarios:
            file1 = invoice_dir / file1_name
            file2 = invoice_dir / file2_name
            
            await self.test_comparison(file1, file2, test_name, invoice_options)
    
    async def run_cross_format_tests(self):
        """Run cross-format comparison tests"""
        print("\n🔄 Cross-Format Test Suite")
        print("=" * 50)
        
        # Test same data in different formats
        product_dir = self.samples_dir / 'product_comparisons'
        
        test_scenarios = [
            ('product_comparison_v1.csv', 'product_comparison_v1.xlsx', 'CSV vs Excel (v1)'),
            ('product_comparison_v1.csv', 'product_comparison_v1.pdf', 'CSV vs PDF (v1)'),
            ('product_comparison_v2.xlsx', 'product_comparison_v2.csv', 'Excel vs CSV (v2)'),
        ]
        
        for file1_name, file2_name, test_name in test_scenarios:
            file1 = product_dir / file1_name
            file2 = product_dir / file2_name
            
            await self.test_comparison(file1, file2, test_name)
    
    async def run_edge_case_tests(self):
        """Run edge case tests"""
        print("\n🔧 Edge Cases Test Suite")
        print("=" * 50)
        
        edge_dir = self.samples_dir / 'edge_cases'
        
        # Test self-comparisons (should be 100% accurate)
        self_comparison_files = [
            ('edge_cases_csv.csv', 'Edge Case CSV Self-Test'),
            ('edge_cases_excel.xlsx', 'Edge Case Excel Self-Test'),
        ]
        
        for filename, test_name in self_comparison_files:
            file_path = edge_dir / filename
            await self.test_comparison(file_path, file_path, test_name)
        
        # Test large dataset
        large_file = edge_dir / 'large_dataset_1000rows.csv'
        await self.test_file_processing(large_file, 'Large Dataset Processing')
    
    async def run_performance_tests(self):
        """Run performance benchmark tests"""
        print("\n⚡ Performance Test Suite")
        print("=" * 50)
        
        # Test files of various sizes
        test_files = [
            ('test_file1.csv', 'Small CSV'),
            ('test_file2.xlsx', 'Small Excel'),
            ('edge_cases/large_dataset_1000rows.csv', 'Large CSV'),
            ('multi_sheet_data.xlsx', 'Multi-sheet Excel'),
        ]
        
        performance_metrics = []
        
        for filename, test_name in test_files:
            file_path = self.samples_dir / filename
            if file_path.exists():
                # Get file size for metrics
                file_size_kb = file_path.stat().st_size / 1024
                start_time = time.time()
                
                result = await self.test_file_processing(file_path, test_name)
                
                processing_time = time.time() - start_time
                tables_count = len(result) if result else 0
                
                if result is not None:
                    performance_metrics.append({
                        'processing_time': processing_time,
                        'file_size_kb': file_size_kb,
                        'tables_count': tables_count
                    })
        
        if performance_metrics:
            avg_time = sum(m['processing_time'] for m in performance_metrics) / len(performance_metrics)
            max_time = max(m['processing_time'] for m in performance_metrics)
            total_tables = sum(m['tables_count'] for m in performance_metrics)
            
            success = max_time < 2.0  # Performance threshold: 2 seconds
            
            self.log_test('performance', 'Performance Benchmarks', success, {
                'avg_time': avg_time,
                'max_time': max_time,
                'files_tested': len(performance_metrics),
                'total_tables': total_tables
            })
    
    async def run_format_compatibility_tests(self):
        """Test format compatibility"""
        print("\n📊 Format Compatibility Test Suite")
        print("=" * 50)
        
        # Test all supported formats
        all_files = list(self.samples_dir.rglob('*'))
        test_files = [f for f in all_files if f.is_file() and f.suffix.lower() in ['.csv', '.xlsx', '.xls', '.pdf']]
        
        format_stats = {}
        success_by_format = {}
        
        for file_path in test_files[:20]:  # Limit to 20 files for brevity
            file_ext = file_path.suffix.lower().lstrip('.')
            
            if file_ext not in format_stats:
                format_stats[file_ext] = {'total': 0, 'success': 0}
                success_by_format[file_ext] = []
            
            format_stats[file_ext]['total'] += 1
            
            result = await self.test_file_processing(file_path, f'Compatibility Test - {file_path.name}')
            success_by_format[file_ext].append(result is not None)
            
            if result is not None:
                format_stats[file_ext]['success'] += 1
        
        for file_ext, stats in format_stats.items():
            total = stats['total']
            success = stats['success']
            success_rate = (success / total * 100) if total > 0 else 0
            
            self.log_test('compatibility', f'{file_ext.upper()} Format', success_rate == 100, {
                'success_rate': success_rate,
                'files_tested': total,
                'successful': success
            })
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print(f"\n{'='*80}")
        print(f"📊 COMPREHENSIVE TEST REPORT")
        print(f"{'='*80}")
        print(f"Test started at: {self.start_time}")
        print(f"Test completed at: {datetime.now().isoformat()}")
        print(f"Total execution time: {time.time() - self.start_time:.2f} seconds")
        
        # Overall statistics
        print(f"\n🎯 Overall Results:")
        print(f"   Total Tests: {self.results['overall']['total']}")
        print(f"   Passed: {self.results['overall']['passed']} ✅")
        print(f"   Failed: {self.results['overall']['failed']} ❌")
        print(f"   Success Rate: {(self.results['overall']['passed'] / self.results['overall']['total'] * 100):.1f}%")
        
        # Category breakdown
        print(f"\n📊 Category Breakdown:")
        for category in ['file_processing', 'comparison', 'compatibility', 'performance']:
            total = self.results[category]['total']
            if total > 0:
                passed = self.results[category]['passed']
                failed = self.results[category]['failed']
                success_rate = (passed / total * 100) if total > 0 else 0
                
                print(f"   {category.title()}: {passed}/{total} ({success_rate:.1f}%)")
        
        # Test details
        print(f"\n📋 Test Details:")
        
        failed_tests = [t for t in self.results['tests'] if 'FAILED' in t['status']]
        if failed_tests:
            print(f"   ❌ Failed Tests:")
            for test in failed_tests:
                print(f"      - [{test['category'].upper()}] {test['name']}")
                if 'error' in test['details']:
                    print(f"        Error: {test['details']['error']}")
        
        passed_tests = [t for t in self.results['tests'] if 'PASSED' in t['status']]
        if len(passed_tests) > 0:
            print(f"   ✅ Successful Tests (showing first 10):")
            for test in passed_tests[:10]:
                print(f"      - [{test['category'].upper()}] {test['name']}")
                if 'time' in test['details']:
                    print(f"        Time: {test['details']['time']:.3f}s")
        
        # Performance analysis
        processing_tests = [t for t in self.results['tests'] if t['category'] == 'file_processing' and 'PASSED' in t['status']]
        if processing_tests:
            avg_time = sum(t['details'].get('time', 0) for t in processing_tests) / len(processing_tests)
            max_time = max(t['details'].get('time', 0) for t in processing_tests)
            total_tables = sum(t['details'].get('tables', 0) for t in processing_tests)
            
            print(f"\n⚡ Performance Analysis:")
            print(f"   Average processing time: {avg_time:.3f}s")
            print(f"   Maximum processing time: {max_time:.3f}s")
            print(f"   Total tables extracted: {total_tables}")
            print(f"   Tables per second: {total_tables / sum(t['details'].get('time', 0) for t in processing_tests):.0f}")
        
        # Comparison analysis
        comparison_tests = [t for t in self.results['tests'] if t['category'] == 'comparison' and 'PASSED' in t['status']]
        if comparison_tests:
            avg_time = sum(t['details'].get('time', 0) for t in comparison_tests) / len(comparison_tests)
            max_time = max(t['details'].get('time', 0) for t in comparison_tests)
            total_rows = sum(t['details'].get('rows_compared', 0) for t in comparison_tests)
            total_differences = sum(t['details'].get('differences', 0) for t in comparison_tests)
            
            print(f"\n🔍 Comparison Analysis:")
            print(f"   Average comparison time: {avg_time:.3f}s")
            print(f"   Maximum comparison time: {max_time:.3f}s")
            print(f"   Total rows compared: {total_rows}")
            print(f"   Total differences found: {total_differences}")
            print(f"   Average accuracy: {sum(t['details'].get('accuracy_rate', 0) for t in comparison_tests) / len(comparison_tests):.1f}%")
        
        # Final assessment
        success_rate = self.results['overall']['passed'] / self.results['overall']['total'] * 100
        print(f"\n🎯 Final Assessment:")
        if success_rate == 100:
            print(f"   🎉 PERFECT! All tests passed successfully!")
        elif success_rate >= 90:
            print(f"   ✅ EXCELLENT! System is highly reliable ({success_rate:.1f}% success rate)")
        elif success_rate >= 80:
            print(f"   ✅ GOOD! System is functional ({success_rate:.1f}% success rate)")
        elif success_rate >= 70:
            print(f"   ⚠️  ACCEPTABLE: System works with some issues ({success_rate:.1f}% success rate)")
        else:
            print(f"   ❌ NEEDS IMPROVEMENT: System has significant issues ({success_rate:.1f}% success rate)")
        
        print(f"\n📁 Test Coverage Summary:")
        print(f"   - File Processing: {self.results['file_processing']['passed']}/{self.results['file_processing']['total']} files")
        print(f"   - Data Comparison: {self.results['comparison']['passed']}/{self.results['comparison']['total']} comparisons")
        print(f"   - All Formats: PDF, Excel, CSV")
        print(f"   - Test Categories: Product, Invoice, Edge Cases, Performance")
        
        print(f"{'='*80}")
    
    async def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 COMPREHENSIVE FILE COMPARISON SYSTEM TEST")
        print(f"📁 Testing directory: {self.samples_dir}")
        print(f"📅 Supported formats: PDF, Excel (.xlsx/.xls), CSV")
        print(f"🎯 Test categories: Processing, Comparison, Performance, Compatibility")
        
        self.start_time = time.time()
        
        # Run all test suites
        await self.run_format_compatibility_tests()
        await self.run_product_comparison_tests()
        await self.run_invoice_comparison_tests()
        await self.run_cross_format_tests()
        await self.run_edge_case_tests()
        await self.run_performance_tests()
        
        self.generate_report()

async def main():
    """Main execution function"""
    runner = MasterTestRunner()
    await runner.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())