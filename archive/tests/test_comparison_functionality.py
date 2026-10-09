#!/usr/bin/env python3
"""
Test comparison functionality with processed data
"""

import os
import sys
import asyncio
import time
from pathlib import Path

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '..', '..', 'backend')
sys.path.insert(0, backend_path)

from backend.processors.csv_processor import CSVProcessor
from backend.processors.excel_processor import ExcelProcessor
from backend.processors.pdf_processor import PDFProcessor
from backend.comparators.data_comparator import DataComparator

class ComparisonTestRunner:
    """Test runner for file comparison functionality"""
    
    def __init__(self):
        self.samples_dir = Path(__file__).parent.parent.parent / 'samples'
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
    
    async def test_comparison(self, file1: Path, file2: Path, test_name: str, options=None):
        """Test comparison between two files"""
        if not file1.exists() or not file2.exists():
            return {
                'test_name': test_name,
                'success': False,
                'error': 'Files not found'
            }
        
        try:
            # Process both files
            data1 = await self.process_file(file1)
            data2 = await self.process_file(file2)
            
            if not data1 or not data2:
                return {
                    'test_name': test_name,
                    'success': False,
                    'error': f'Failed to extract data: data1={len(data1)}, data2={len(data2)}'
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
            
            success = True  # Comparison completed successfully
            
            return {
                'test_name': test_name,
                'success': success,
                'comparison_time': comparison_time,
                'total_rows': summary.get('total_rows_compared', 0),
                'matching_rows': summary.get('matching_rows', 0),
                'different_rows': summary.get('different_rows', 0),
                'accuracy_rate': summary.get('accuracy_rate', 0),
                'differences_found': len(differences),
                'file1_tables': len(data1),
                'file2_tables': len(data2),
                'error': None
            }
            
        except Exception as e:
            return {
                'test_name': test_name,
                'success': False,
                'error': str(e)
            }
    
    async def test_product_comparisons(self):
        """Test product comparison scenarios"""
        print("\n🔍 Testing Product Comparisons")
        print("-" * 40)
        
        # Test CSV files
        csv_v1 = self.samples_dir / 'product_comparisons' / 'product_comparison_v1.csv'
        csv_v2 = self.samples_dir / 'product_comparisons' / 'product_comparison_v2.csv'
        
        if csv_v1.exists() and csv_v2.exists():
            result = await self.test_comparison(
                csv_v1, csv_v2, 
                "Product Comparison (CSV)"
            )
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
        
        # Test Excel files
        excel_v1 = self.samples_dir / 'product_comparisons' / 'product_comparison_v1.xlsx'
        excel_v2 = self.samples_dir / 'product_comparisons' / 'product_comparison_v2.xlsx'
        
        if excel_v1.exists() and excel_v2.exists():
            result = await self.test_comparison(
                excel_v1, excel_v2,
                "Product Comparison (Excel)"
            )
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    async def test_invoice_comparisons(self):
        """Test invoice comparison scenarios"""
        print("\n🧾 Testing Invoice Comparisons")
        print("-" * 40)
        
        # Test with invoice options
        invoice_options = {
            'comparison_type': 'invoices',
            'exact_match': False,
            'tolerance_settings': {
                'quantity': 0.05,
                'unit_price': 0.005,
                'amount': 0.005
            }
        }
        
        # Test CSV files
        inv1_csv = self.samples_dir / 'invoice_comparisons' / 'invoice_001.csv'
        inv2_csv = self.samples_dir / 'invoice_comparisons' / 'invoice_002.csv'
        
        if inv1_csv.exists() and inv2_csv.exists():
            result = await self.test_comparison(
                inv1_csv, inv2_csv,
                "Invoice Comparison (CSV)",
                invoice_options
            )
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
        
        # Test Excel files
        inv1_excel = self.samples_dir / 'invoice_comparisons' / 'invoice_001.xlsx'
        inv2_excel = self.samples_dir / 'invoice_comparisons' / 'invoice_002.xlsx'
        
        if inv1_excel.exists() and inv2_excel.exists():
            result = await self.test_comparison(
                inv1_excel, inv2_excel,
                "Invoice Comparison (Excel)",
                invoice_options
            )
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    async def test_cross_format_comparisons(self):
        """Test comparisons between different file formats"""
        print("\n🔄 Testing Cross-Format Comparisons")
        print("-" * 40)
        
        # Test CSV vs Excel
        csv_file = self.samples_dir / 'product_comparisons' / 'product_comparison_v1.csv'
        excel_file = self.samples_dir / 'product_comparisons' / 'product_comparison_v1.xlsx'
        
        if csv_file.exists() and excel_file.exists():
            result = await self.test_comparison(
                csv_file, excel_file,
                "CSV vs Excel Comparison"
            )
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Should have high accuracy (same data)")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
        
        # Test Excel vs CSV (different versions)
        excel_v2 = self.samples_dir / 'product_comparisons' / 'product_comparison_v2.xlsx'
        csv_v2 = self.samples_dir / 'product_comparisons' / 'product_comparison_v2.csv'
        
        if excel_v2.exists() and csv_v2.exists():
            result = await self.test_comparison(
                excel_v2, csv_v2,
                "Excel vs CSV Comparison (v2)"
            )
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Should have high accuracy (same data)")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    async def test_edge_case_comparisons(self):
        """Test comparisons with edge cases"""
        print("\n🔧 Testing Edge Case Comparisons")
        print("-" * 40)
        
        # Test edge cases files with themselves (should be identical)
        edge_csv = self.samples_dir / 'edge_cases' / 'edge_cases_csv.csv'
        edge_excel = self.samples_dir / 'edge_cases' / 'edge_cases_excel.xlsx'
        
        if edge_csv.exists():
            result = await self.test_comparison(
                edge_csv, edge_csv,
                "Edge Case Self-Comparison (CSV)"
            )
            self.results.append(result)
            
            if result['success']:
                expected_accuracy = 100.0
                if abs(result['accuracy_rate'] - expected_accuracy) < 1.0:  # Allow small tolerance
                    print(f"   ✅ {result['test_name']} - Perfect match as expected")
                else:
                    print(f"   ⚠️  {result['test_name']} - Expected 100% but got {result['accuracy_rate']:.1f}%")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
        
        if edge_excel.exists():
            result = await self.test_comparison(
                edge_excel, edge_excel,
                "Edge Case Self-Comparison (Excel)"
            )
            self.results.append(result)
            
            if result['success']:
                expected_accuracy = 100.0
                if abs(result['accuracy_rate'] - expected_accuracy) < 1.0:  # Allow small tolerance
                    print(f"   ✅ {result['test_name']} - Perfect match as expected")
                else:
                    print(f"   ⚠️  {result['test_name']} - Expected 100% but got {result['accuracy_rate']:.1f}%")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    def print_summary(self):
        """Print comparison test summary"""
        print(f"\n{'='*60}")
        print(f"📊 COMPARISON TEST SUMMARY")
        print(f"{'='*60}")
        
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
        
        # Expected results analysis
        print(f"\n🎯 Expected vs Actual Results:")
        
        expected_tests = {
            "Product Comparison (CSV)": {"differences": ">=3", "accuracy": "<100"},
            "Product Comparison (Excel)": {"differences": ">=3", "accuracy": "<100"},
            "Invoice Comparison (CSV)": {"differences": ">=3", "accuracy": "<100"},
            "Invoice Comparison (Excel)": {"differences": ">=3", "accuracy": "<100"},
            "CSV vs Excel Comparison": {"accuracy": ">95"},
            "Excel vs CSV Comparison (v2)": {"accuracy": ">95"},
            "Edge Case Self-Comparison (CSV)": {"accuracy": "≈100"},
            "Edge Case Self-Comparison (Excel)": {"accuracy": "≈100"}
        }
        
        for test in self.results:
            if test['success'] and test['test_name'] in expected_tests:
                expected = expected_tests[test['test_name']]
                
                if 'differences' in expected:
                    expected_diff = expected['differences']
                    actual_diff = test['differences_found']
                    
                    if isinstance(expected_diff, int) and expected_diff >= 0:
                        if actual_diff >= expected_diff:
                            print(f"   ✅ {test['test_name']}: Found {actual_diff} differences (expected >= {expected_diff})")
                        else:
                            print(f"   ⚠️  {test['test_name']}: Found {actual_diff} differences (expected >= {expected_diff})")
                
                if 'accuracy' in expected:
                    expected_acc = expected['accuracy']
                    actual_acc = test['accuracy_rate']
                    
                    if expected_acc == "<100" and actual_acc < 100:
                        print(f"   ✅ {test['test_name']}: Accuracy {actual_acc:.1f}% (expected <100%)")
                    elif expected_acc == ">95" and actual_acc > 95:
                        print(f"   ✅ {test['test_name']}: Accuracy {actual_acc:.1f}% (expected >95%)")
                    elif expected_acc == "≈100" and abs(actual_acc - 100) < 5:
                        print(f"   ✅ {test['test_name']}: Accuracy {actual_acc:.1f}% (expected ≈100%)")
                    else:
                        print(f"   ❓ {test['test_name']}: Accuracy {actual_acc:.1f}% (expected {expected_acc})")
        
        if failed_tests == 0:
            print(f"\n🎉 ALL COMPARISON TESTS PASSED!")
        elif successful_tests / total_tests >= 0.8:
            print(f"\n✅ GOOD PERFORMANCE! Most comparison tests passed.")
        else:
            print(f"\n⚠️  Some comparison issues detected.")
        
        print(f"{'='*60}")
    
    async def run_all_tests(self):
        """Run all comparison tests"""
        print("🚀 Starting File Comparison Tests")
        print(f"Testing files from: {self.samples_dir}")
        
        start_time = time.time()
        
        await self.test_product_comparisons()
        await self.test_invoice_comparisons()
        await self.test_cross_format_comparisons()
        await self.test_edge_case_comparisons()
        
        total_time = time.time() - start_time
        print(f"\n⏱️  Total test execution time: {total_time:.2f} seconds")
        self.print_summary()

async def main():
    """Main function"""
    runner = ComparisonTestRunner()
    await runner.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())