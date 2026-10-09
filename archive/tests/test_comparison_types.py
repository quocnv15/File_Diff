#!/usr/bin/env python3
"""
Test comparison functionality with different file types
"""

import os
import sys
import asyncio
import time
from pathlib import Path

# Add backend directory to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

from backend.processors.csv_processor import CSVProcessor
from backend.processors.excel_processor import ExcelProcessor
from backend.processors.pdf_processor import PDFProcessor
from backend.comparators.data_comparator import DataComparator

class ComparisonTypeTestRunner:
    """Test runner for comparing different file types"""
    
    def __init__(self):
        self.samples_dir = Path.cwd() / 'samples'
        self.processors = {
            'csv': CSVProcessor(),
            'xlsx': ExcelProcessor(),
            'pdf': PDFProcessor()
        }
        self.comparator = DataComparator()
        self.results = []
    
    async def process_file(self, file_path: Path):
        """Process a single file"""
        file_ext = file_path.suffix.lower().lstrip('.')
        if file_ext not in self.processors:
            return None
        
        processor = self.processors[file_ext]
        result = await processor.process(str(file_path))
        return result.get('structured_data', [])
    
    async def test_file_comparison(self, file1_path: Path, file2_path: Path, test_name: str, options=None):
        """Test comparison between two files"""
        if not file1_path.exists() or not file2_path.exists():
            return {
                'test_name': test_name,
                'success': False,
                'error': 'Files not found'
            }
        
        try:
            # Process both files
            data1 = await self.process_file(file1_path)
            data2 = await self.process_file(file2_path)
            
            if not data1 or not data2:
                return {
                    'test_name': test_name,
                    'success': False,
                    'error': f'Failed to extract data: data1={len(data1) if data1 else 0}, data2={len(data2) if data2 else 0}'
                }
            
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
            
            return {
                'test_name': test_name,
                'success': True,
                'comparison_time': comparison_time,
                'total_rows': summary.get('total_rows_compared', 0),
                'matching_rows': summary.get('matching_rows', 0),
                'different_rows': summary.get('different_rows', 0),
                'accuracy_rate': summary.get('accuracy_rate', 0),
                'differences_found': len(differences),
                'file1_tables': len(data1),
                'file2_tables': len(data2),
                'error': None,
                'file1_type': file1_path.suffix,
                'file2_type': file2_path.suffix
            }
            
        except Exception as e:
            return {
                'test_name': test_name,
                'success': False,
                'error': str(e)
            }
    
    async def test_same_format_comparisons(self):
        """Test comparisons between same file formats"""
        print("\n🔄 Testing Same Format Comparisons")
        print("=" * 50)
        
        test_scenarios = [
            # CSV comparisons
            ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v2.csv', 'CSV Product Comparison'),
            ('invoice_comparisons/invoice_001.csv', 'invoice_comparisons/invoice_002.csv', 'CSV Invoice Comparison'),
            
            # Excel comparisons
            ('product_comparisons/product_comparison_v1.xlsx', 'product_comparisons/product_comparison_v2.xlsx', 'Excel Product Comparison'),
            ('invoice_comparisons/invoice_001.xlsx', 'invoice_comparisons/invoice_002.xlsx', 'Excel Invoice Comparison'),
            
            # PDF comparisons
            ('product_comparisons/product_comparison_v1.pdf', 'product_comparisons/product_comparison_v2.pdf', 'PDF Product Comparison'),
            ('invoice_comparisons/invoice_001.pdf', 'invoice_comparisons/invoice_002.pdf', 'PDF Invoice Comparison'),
        ]
        
        for file1, file2, test_name in test_scenarios:
            file1_path = self.samples_dir / file1
            file2_path = self.samples_dir / file2
            
            result = await self.test_file_comparison(file1_path, file2_path, test_name)
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Format: {result['file1_type'].upper()} vs {result['file2_type'].upper()}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    async def test_cross_format_comparisons(self):
        """Test comparisons between different file formats"""
        print("\n🔄 Testing Cross-Format Comparisons")
        print("=" * 50)
        
        test_scenarios = [
            # CSV vs Excel (same data)
            ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v1.xlsx', 'CSV vs Excel (v1)'),
            ('product_comparisons/product_comparison_v2.csv', 'product_comparisons/product_comparison_v2.xlsx', 'CSV vs Excel (v2)'),
            
            # CSV vs PDF
            ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v1.pdf', 'CSV vs PDF (v1)'),
            
            # Excel vs PDF
            ('product_comparisons/product_comparison_v1.xlsx', 'product_comparisons/product_comparison_v1.pdf', 'Excel vs PDF (v1)'),
            
            # Invoice cross-format
            ('invoice_comparisons/invoice_001.csv', 'invoice_comparisons/invoice_001.xlsx', 'Invoice CSV vs Excel'),
        ]
        
        for file1, file2, test_name in test_scenarios:
            file1_path = self.samples_dir / file1
            file2_path = self.samples_dir / file2
            
            result = await self.test_file_comparison(file1_path, file2_path, test_name)
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Format: {result['file1_type'].upper()} vs {result['file2_type'].upper()}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    async def test_self_comparisons(self):
        """Test self-comparisons (should be 100% accurate)"""
        print("\n🔍 Testing Self-Comparisons")
        print("=" * 50)
        
        test_files = [
            'edge_cases/edge_cases_csv.csv',
            'edge_cases/edge_cases_excel.xlsx',
            'test_file1.csv',
            'test_file1.xlsx'
        ]
        
        for file_name in test_files:
            file_path = self.samples_dir / file_name
            if file_path.exists():
                result = await self.test_file_comparison(file_path, file_path, f"Self-Comparison: {file_name}")
                self.results.append(result)
                
                if result['success']:
                    expected_accuracy = 100.0
                    actual_accuracy = result['accuracy_rate']
                    
                    if abs(actual_accuracy - expected_accuracy) < 1.0:
                        print(f"   ✅ {result['test_name']} - Perfect match!")
                    else:
                        print(f"   ⚠️  {result['test_name']} - Expected 100% but got {actual_accuracy:.1f}%")
                    
                    print(f"      - Format: {result['file1_type'].upper()}")
                    print(f"      - Accuracy: {actual_accuracy:.1f}%")
                    print(f"      - Time: {result['comparison_time']:.3f}s")
                else:
                    print(f"   ❌ {result['test_name']} - {result['error']}")
    
    async def test_invoice_specific_options(self):
        """Test invoice comparisons with invoice-specific options"""
        print("\n🧾 Testing Invoice-Specific Comparisons")
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
            ('invoice_comparisons/invoice_001.csv', 'invoice_comparisons/invoice_002.csv', 'Invoice CSV (Invoice Options)'),
            ('invoice_comparisons/invoice_001.xlsx', 'invoice_comparisons/invoice_002.xlsx', 'Invoice Excel (Invoice Options)'),
        ]
        
        for file1, file2, test_name in test_scenarios:
            file1_path = self.samples_dir / file1
            file2_path = self.samples_dir / file2
            
            result = await self.test_file_comparison(file1_path, file2_path, test_name, invoice_options)
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Format: {result['file1_type'].upper()} vs {result['file2_type'].upper()}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    def print_summary(self):
        """Print comprehensive comparison test summary"""
        print(f"\n{'='*80}")
        print(f"📊 COMPARISON TYPE TEST SUMMARY")
        print(f"{'='*80}")
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"Total Comparison Tests: {total_tests}")
        print(f"Successful: {successful_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(successful_tests / total_tests * 100):.1f}%")
        
        if successful_tests > 0:
            total_rows = sum(r['total_rows'] for r in self.results if r['success'])
            total_differences = sum(r['differences_found'] for r in self.results if r['success'])
            avg_time = sum(r['comparison_time'] for r in self.results if r['success']) / successful_tests
            avg_accuracy = sum(r['accuracy_rate'] for r in self.results if r['success']) / successful_tests
            
            print(f"Total Rows Compared: {total_rows}")
            print(f"Total Differences Found: {total_differences}")
            print(f"Average Comparison Time: {avg_time:.3f}s")
            print(f"Average Accuracy: {avg_accuracy:.1f}%")
        
        # Group by file type combinations
        print(f"\n📊 Results by Format Combination:")
        format_combinations = {}
        
        for result in self.results:
            if result['success']:
                key = f"{result['file1_type'].upper()} vs {result['file2_type'].upper()}"
                if key not in format_combinations:
                    format_combinations[key] = {'count': 0, 'total_accuracy': 0, 'total_time': 0}
                
                format_combinations[key]['count'] += 1
                format_combinations[key]['total_accuracy'] += result['accuracy_rate']
                format_combinations[key]['total_time'] += result['comparison_time']
        
        for combo, stats in format_combinations.items():
            avg_accuracy = stats['total_accuracy'] / stats['count']
            avg_time = stats['total_time'] / stats['count']
            print(f"   - {combo}: {stats['count']} tests, avg accuracy {avg_accuracy:.1f}%, avg time {avg_time:.3f}s")
        
        # Show failed tests
        failed_results = [r for r in self.results if not r['success']]
        if failed_results:
            print(f"\n❌ Failed Tests:")
            for result in failed_results:
                print(f"   - {result['test_name']}: {result['error']}")
        
        if failed_tests == 0:
            print(f"\n🎉 ALL COMPARISON TESTS PASSED!")
        elif successful_tests / total_tests >= 0.8:
            print(f"\n✅ GOOD PERFORMANCE! Most comparison tests passed.")
        else:
            print(f"\n⚠️  Some comparison issues detected.")
        
        print(f"{'='*80}")
    
    async def run_all_tests(self):
        """Run all comparison type tests"""
        print("🚀 Starting File Comparison Type Tests")
        print(f"Testing files from: {self.samples_dir}")
        
        start_time = time.time()
        
        await self.test_same_format_comparisons()
        await self.test_cross_format_comparisons()
        await self.test_self_comparisons()
        await self.test_invoice_specific_options()
        
        total_time = time.time() - start_time
        print(f"\n⏱️  Total test execution time: {total_time:.2f} seconds")
        self.print_summary()

async def main():
    """Main function"""
    runner = ComparisonTypeTestRunner()
    await runner.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())