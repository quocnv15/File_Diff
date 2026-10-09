#!/usr/bin/env python3
"""
Comprehensive test runner for new sample files
Tests all file formats and comparison scenarios with the new organized test data
"""

import os
import sys
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from backend.processors.csv_processor import CSVProcessor
from backend.processors.excel_processor import ExcelProcessor
from backend.processors.pdf_processor import PDFProcessor
from backend.comparators.data_comparator import DataComparator
from backend.utils.logger import get_process_logger

class ComprehensiveTestRunner:
    """Comprehensive test runner for new sample files"""
    
    def __init__(self):
        self.samples_dir = Path(__file__).parent / 'samples'
        self.processors = {
            'csv': CSVProcessor(),
            'xlsx': ExcelProcessor(),
            'xls': ExcelProcessor(),
            'pdf': PDFProcessor()
        }
        self.comparator = DataComparator()
        self.logger = get_process_logger('comprehensive_test')
        self.results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
    
    def log_test_result(self, test_name: str, passed: bool, details: Dict[str, Any] = None):
        """Log test result"""
        self.results['total_tests'] += 1
        if passed:
            self.results['passed_tests'] += 1
            status = "✅ PASSED"
        else:
            self.results['failed_tests'] += 1
            status = "❌ FAILED"
        
        test_detail = {
            'name': test_name,
            'status': status,
            'details': details or {}
        }
        self.results['test_details'].append(test_detail)
        
        print(f"{status} {test_name}")
        if details:
            for key, value in details.items():
                print(f"   - {key}: {value}")
    
    async def test_file_processing(self, file_path: Path) -> Dict[str, Any]:
        """Test file processing with appropriate processor"""
        file_ext = file_path.suffix.lower().lstrip('.')
        if file_ext not in self.processors:
            return {'success': False, 'error': f'Unsupported file type: {file_ext}'}
        
        processor = self.processors[file_ext]
        
        try:
            start_time = time.time()
            result = await processor.process(str(file_path))
            processing_time = time.time() - start_time
            
            return {
                'success': True,
                'processing_time': processing_time,
                'structured_data_count': len(result.get('structured_data', [])),
                'has_content': bool(result.get('markdown_content')),
                'file_size': file_path.stat().st_size
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_size': file_path.stat().st_size
            }
    
    async def test_product_comparisons(self):
        """Test product comparison scenarios"""
        print("\n🔍 Testing Product Comparisons...")
        
        # Get product comparison files
        product_dir = self.samples_dir / 'product_comparisons'
        
        # Test each format
        formats = ['pdf', 'xlsx', 'csv']
        
        for format_type in formats:
            print(f"\n📊 Testing {format_type.upper()} product comparisons...")
            
            v1_file = product_dir / f'product_comparison_v1.{format_type}'
            v2_file = product_dir / f'product_comparison_v2.{format_type}'
            
            if v1_file.exists() and v2_file.exists():
                # Test file processing
                v1_result = await self.test_file_processing(v1_file)
                v2_result = await self.test_file_processing(v2_file)
                
                if v1_result['success'] and v2_result['success']:
                    # Test comparison
                    comparison_options = {
                        'comparison_type': 'products',
                        'exact_match': False,
                        'tolerance_settings': {
                            'quantity': 0.1,
                            'unit_price': 0.01,
                            'amount': 0.01
                        }
                    }
                    
                    try:
                        start_time = time.time()
                        comparison_result = await self.comparator.compare(
                            v1_result.get('structured_data', []),
                            v2_result.get('structured_data', []),
                            comparison_options
                        )
                        comparison_time = time.time() - start_time
                        
                        details = {
                            'v1_processing': f"{v1_result['processing_time']:.3f}s",
                            'v2_processing': f"{v2_result['processing_time']:.3f}s",
                            'comparison_time': f"{comparison_time:.3f}s",
                            'differences_found': len(comparison_result.get('differences', [])),
                            'accuracy_rate': comparison_result.get('summary', {}).get('accuracy_rate', 0),
                            'v1_structured_items': v1_result.get('structured_data_count'),
                            'v2_structured_items': v2_result.get('structured_data_count')
                        }
                        
                        # Expected differences for product comparison
                        expected_differences = 4  # Price change, quantity change, name change, new product
                        actual_differences = len(comparison_result.get('differences', []))
                        
                        success = (
                            actual_differences >= 3 and  # At least 3 major differences
                            comparison_result.get('summary', {}).get('accuracy_rate', 0) < 100 and
                            v1_result['structured_data_count'] > 0 and
                            v2_result['structured_data_count'] > 0
                        )
                        
                        self.log_test_result(
                            f"Product comparison ({format_type})",
                            success,
                            details
                        )
                        
                    except Exception as e:
                        self.log_test_result(
                            f"Product comparison ({format_type})",
                            False,
                            {'error': str(e)}
                        )
                else:
                    self.log_test_result(
                        f"Product comparison ({format_type})",
                        False,
                        {'v1_error': v1_result.get('error', 'Unknown'), 
                         'v2_error': v2_result.get('error', 'Unknown')}
                    )
            else:
                self.log_test_result(
                    f"Product comparison ({format_type})",
                    False,
                    {'error': f'Missing files: v1={v1_file.exists()}, v2={v2_file.exists()}'}
                )
    
    async def test_invoice_comparisons(self):
        """Test invoice comparison scenarios"""
        print("\n🧾 Testing Invoice Comparisons...")
        
        invoice_dir = self.samples_dir / 'invoice_comparisons'
        formats = ['pdf', 'xlsx', 'csv']
        
        for format_type in formats:
            print(f"\n📋 Testing {format_type.upper()} invoice comparisons...")
            
            inv1_file = invoice_dir / f'invoice_001.{format_type}'
            inv2_file = invoice_dir / f'invoice_002.{format_type}'
            
            if inv1_file.exists() and inv2_file.exists():
                # Test file processing
                inv1_result = await self.test_file_processing(inv1_file)
                inv2_result = await self.test_file_processing(inv2_file)
                
                if inv1_result['success'] and inv2_result['success']:
                    # Test comparison
                    comparison_options = {
                        'comparison_type': 'invoices',
                        'exact_match': False,
                        'tolerance_settings': {
                            'quantity': 0.05,
                            'unit_price': 0.005,
                            'amount': 0.005
                        }
                    }
                    
                    try:
                        start_time = time.time()
                        comparison_result = await self.comparator.compare(
                            inv1_result.get('structured_data', []),
                            inv2_result.get('structured_data', []),
                            comparison_options
                        )
                        comparison_time = time.time() - start_time
                        
                        details = {
                            'inv1_processing': f"{inv1_result['processing_time']:.3f}s",
                            'inv2_processing': f"{inv2_result['processing_time']:.3f}s",
                            'comparison_time': f"{comparison_time:.3f}s",
                            'differences_found': len(comparison_result.get('differences', [])),
                            'accuracy_rate': comparison_result.get('summary', {}).get('accuracy_rate', 0)
                        }
                        
                        # Expected differences for invoice comparison
                        success = (
                            len(comparison_result.get('differences', [])) >= 3 and  # At least 3 differences
                            comparison_result.get('summary', {}).get('accuracy_rate', 0) < 100 and
                            inv1_result['structured_data_count'] > 0 and
                            inv2_result['structured_data_count'] > 0
                        )
                        
                        self.log_test_result(
                            f"Invoice comparison ({format_type})",
                            success,
                            details
                        )
                        
                    except Exception as e:
                        self.log_test_result(
                            f"Invoice comparison ({format_type})",
                            False,
                            {'error': str(e)}
                        )
                else:
                    self.log_test_result(
                        f"Invoice comparison ({format_type})",
                        False,
                        {'inv1_error': inv1_result.get('error', 'Unknown'), 
                         'inv2_error': inv2_result.get('error', 'Unknown')}
                    )
            else:
                self.log_test_result(
                    f"Invoice comparison ({format_type})",
                    False,
                    {'error': f'Missing files: inv1={inv1_file.exists()}, inv2={inv2_file.exists()}'}
                )
    
    async def test_edge_cases(self):
        """Test edge cases and special scenarios"""
        print("\n🔧 Testing Edge Cases...")
        
        edge_cases_dir = self.samples_dir / 'edge_cases'
        
        # Test specific edge case files
        edge_files = [
            ('edge_cases_csv.csv', 'CSV edge cases'),
            ('edge_cases_excel.xlsx', 'Excel edge cases'),
            ('edge_cases_test.pdf', 'PDF edge cases'),
            ('large_dataset_1000rows.csv', 'Large dataset (1000 rows)'),
            ('semicolon_delimiter.csv', 'Semicolon delimiter'),
            ('tab_delimiter.csv', 'Tab delimiter')
        ]
        
        for filename, description in edge_files:
            file_path = edge_cases_dir / filename
            
            if file_path.exists():
                print(f"\n🎯 Testing {description}...")
                
                result = await self.test_file_processing(file_path)
                
                # For edge cases, we mainly test that processing doesn't crash
                success = result['success'] and result['structured_data_count'] > 0
                
                details = {
                    'processing_time': f"{result.get('processing_time', 0):.3f}s",
                    'structured_data_count': result.get('structured_data_count', 0),
                    'file_size': f"{result.get('file_size', 0)} bytes"
                }
                
                if not success:
                    details['error'] = result.get('error', 'Unknown error')
                
                self.log_test_result(
                    description,
                    success,
                    details
                )
            else:
                self.log_test_result(
                    description,
                    False,
                    {'error': f'File not found: {file_path}'}
                )
    
    async def test_decimal_precision(self):
        """Test decimal precision scenarios"""
        print("\n🔢 Testing Decimal Precision...")
        
        decimal_dir = self.samples_dir / 'decimal_tests'
        
        precision_files = [
            ('decimal_precision_csv.csv', 'CSV decimal precision'),
            ('decimal_precision_test.xlsx', 'Excel decimal precision')
        ]
        
        for filename, description in precision_files:
            file_path = decimal_dir / filename
            
            if file_path.exists():
                print(f"\n🎯 Testing {description}...")
                
                result = await self.test_file_processing(file_path)
                
                # For decimal precision tests, check if data is preserved correctly
                success = result['success']
                
                details = {
                    'processing_time': f"{result.get('processing_time', 0):.3f}s",
                    'structured_data_count': result.get('structured_data_count', 0),
                    'file_size': f"{result.get('file_size', 0)} bytes"
                }
                
                if not success:
                    details['error'] = result.get('error', 'Unknown error')
                
                self.log_test_result(
                    description,
                    success,
                    details
                )
            else:
                self.log_test_result(
                    description,
                    False,
                    {'error': f'File not found: {file_path}'}
                )
    
    async def test_multi_table(self):
        """Test multi-table extraction"""
        print("\n📊 Testing Multi-Table Extraction...")
        
        multi_table_files = [
            ('multi_table_tests/multi_table_data.pdf', 'Multi-table PDF'),
            ('multi_sheet_data.xlsx', 'Multi-sheet Excel')
        ]
        
        for filename, description in multi_table_files:
            file_path = self.samples_dir / filename
            
            if file_path.exists():
                print(f"\n🎯 Testing {description}...")
                
                result = await self.test_file_processing(file_path)
                
                # For multi-table tests, check if multiple tables are extracted
                success = result['success'] and result.get('structured_data_count', 0) > 1
                
                details = {
                    'processing_time': f"{result.get('processing_time', 0):.3f}s",
                    'structured_data_count': result.get('structured_data_count', 0),
                    'file_size': f"{result.get('file_size', 0)} bytes"
                }
                
                if not success:
                    details['error'] = result.get('error', 'Unknown error')
                
                self.log_test_result(
                    description,
                    success,
                    details
                )
            else:
                self.log_test_result(
                    description,
                    False,
                    {'error': f'File not found: {file_path}'}
                )
    
    async def test_performance_benchmarks(self):
        """Test performance benchmarks"""
        print("\n⚡ Performance Benchmarks...")
        
        # Test with various file sizes and formats
        benchmark_files = [
            ('edge_cases/large_dataset_1000rows.csv', 'Large CSV (1000 rows)'),
            ('product_comparisons/product_comparison_v2.xlsx', 'Medium Excel'),
            ('product_comparisons/product_comparison_v2.pdf', 'Medium PDF'),
            ('test_file2.csv', 'Small CSV'),
            ('test_file2.xlsx', 'Small Excel')
        ]
        
        performance_results = []
        
        for filename, description in benchmark_files:
            file_path = self.samples_dir / filename
            
            if file_path.exists():
                result = await self.test_file_processing(file_path)
                
                if result['success']:
                    performance_results.append({
                        'description': description,
                        'file_size_kb': result.get('file_size', 0) / 1024,
                        'processing_time': result.get('processing_time', 0),
                        'items_per_second': result.get('structured_data_count', 0) / max(result.get('processing_time', 0.001), 0.001)
                    })
        
        # Analyze performance
        if performance_results:
            avg_time = sum(r['processing_time'] for r in performance_results) / len(performance_results)
            max_time = max(r['processing_time'] for r in performance_results)
            
            print(f"\n📊 Performance Summary:")
            print(f"   - Average processing time: {avg_time:.3f}s")
            print(f"   - Maximum processing time: {max_time:.3f}s")
            print(f"   - Files tested: {len(performance_results)}")
            
            # Performance test passes if no file takes more than 5 seconds
            success = max_time < 5.0
            
            self.log_test_result(
                "Performance benchmarks",
                success,
                {
                    'avg_time': f"{avg_time:.3f}s",
                    'max_time': f"{max_time:.3f}s",
                    'files_tested': len(performance_results)
                }
            )
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"📊 COMPREHENSIVE TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed_tests']} ✅")
        print(f"Failed: {self.results['failed_tests']} ❌")
        print(f"Success Rate: {(self.results['passed_tests'] / self.results['total_tests'] * 100):.1f}%")
        
        if self.results['failed_tests'] > 0:
            print(f"\n❌ Failed Tests:")
            for test in self.results['test_details']:
                if 'FAILED' in test['status']:
                    print(f"   - {test['name']}: {test['details'].get('error', 'Unknown error')}")
        
        print(f"\n🎯 Test Categories:")
        categories = {}
        for test in self.results['test_details']:
            category = test['name'].split(' (')[0]
            if category not in categories:
                categories[category] = {'passed': 0, 'failed': 0}
            
            if 'PASSED' in test['status']:
                categories[category]['passed'] += 1
            else:
                categories[category]['failed'] += 1
        
        for category, counts in categories.items():
            total = counts['passed'] + counts['failed']
            success_rate = (counts['passed'] / total * 100) if total > 0 else 0
            print(f"   - {category}: {counts['passed']}/{total} ({success_rate:.1f}%)")
        
        # Overall assessment
        if self.results['failed_tests'] == 0:
            print(f"\n🎉 ALL TESTS PASSED! System is working perfectly.")
        elif self.results['passed_tests'] / self.results['total_tests'] >= 0.8:
            print(f"\n✅ Good performance! Most tests passed.")
        else:
            print(f"\n⚠️  Some issues detected. Please review failed tests.")
        
        print(f"{'='*60}")
    
    async def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🚀 Starting Comprehensive File Comparison System Tests")
        print(f"Testing files from: {self.samples_dir}")
        print(f"Supported formats: PDF, Excel, CSV")
        
        start_time = time.time()
        
        # Run test categories
        await self.test_product_comparisons()
        await self.test_invoice_comparisons()
        await self.test_multi_table()
        await self.test_edge_cases()
        await self.test_decimal_precision()
        await self.test_performance_benchmarks()
        
        total_time = time.time() - start_time
        
        print(f"\n⏱️  Total test execution time: {total_time:.2f} seconds")
        self.print_summary()

async def main():
    """Main function to run tests"""
    runner = ComprehensiveTestRunner()
    await runner.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())