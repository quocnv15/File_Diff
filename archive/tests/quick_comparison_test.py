#!/usr/bin/env python3
"""
Quick comparison test with different file types
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

async def quick_comparison_test():
    """Quick test of comparison functionality"""
    print("🚀 Quick Comparison Test with Different File Types")
    print("=" * 60)
    
    samples_dir = Path.cwd() / 'samples'
    processors = {
        'csv': CSVProcessor(),
        'xlsx': ExcelProcessor(),
        'pdf': PDFProcessor()
    }
    comparator = DataComparator()
    
    # Test same format comparisons
    test_cases = [
        ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v2.csv', 'CSV vs CSV'),
        ('product_comparisons/product_comparison_v1.xlsx', 'product_comparisons/product_comparison_v2.xlsx', 'Excel vs Excel'),
        ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v1.xlsx', 'CSV vs Excel'),
    ]
    
    results = []
    
    for file1, file2, test_name in test_cases:
        print(f"\n📊 Testing: {test_name}")
        
        try:
            # Process first file
            file1_path = samples_dir / file1
            file1_ext = file1_path.suffix.lower().lstrip('.')
            processor1 = processors[file1_ext]
            data1 = await processor1.process(str(file1_path))
            tables1 = data1.get('structured_data', [])
            
            # Process second file
            file2_path = samples_dir / file2
            file2_ext = file2_path.suffix.lower().lstrip('.')
            processor2 = processors[file2_ext]
            data2 = await processor2.process(str(file2_path))
            tables2 = data2.get('structured_data', [])
            
            if not tables1 or not tables2:
                print(f"   ❌ Failed to extract data from files")
                continue
            
            # Compare
            start_time = time.time()
            comparison_result = await comparator.compare(tables1, tables2, {
                'comparison_type': 'products',
                'exact_match': False,
                'tolerance_settings': {'quantity': 0.1, 'unit_price': 0.01, 'amount': 0.01}
            })
            comparison_time = time.time() - start_time
            
            summary = comparison_result.get('summary', {})
            differences = comparison_result.get('differences', [])
            
            print(f"   ✅ {test_name}")
            print(f"      - File1: {file1_ext.upper()} ({len(tables1)} tables)")
            print(f"      - File2: {file2_ext.upper()} ({len(tables2)} tables)")
            print(f"      - Rows compared: {summary.get('total_rows_compared', 0)}")
            print(f"      - Differences found: {len(differences)}")
            print(f"      - Accuracy rate: {summary.get('accuracy_rate', 0):.1f}%")
            print(f"      - Comparison time: {comparison_time:.3f}s")
            
            results.append({
                'test_name': test_name,
                'success': True,
                'file1_type': file1_ext.upper(),
                'file2_type': file2_ext.upper(),
                'accuracy': summary.get('accuracy_rate', 0),
                'differences': len(differences),
                'time': comparison_time
            })
            
        except Exception as e:
            print(f"   ❌ {test_name}: {str(e)}")
            results.append({
                'test_name': test_name,
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 QUICK COMPARISON TEST SUMMARY")
    print(f"{'='*60}")
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r['success'])
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests} ✅")
    print(f"Failed: {total_tests - successful_tests} ❌")
    print(f"Success Rate: {(successful_tests / total_tests * 100):.1f}%")
    
    if successful_tests > 0:
        successful_results = [r for r in results if r['success']]
        avg_accuracy = sum(r['accuracy'] for r in successful_results) / len(successful_results)
        avg_time = sum(r['time'] for r in successful_results) / len(successful_results)
        total_differences = sum(r['differences'] for r in successful_results)
        
        print(f"Average Accuracy: {avg_accuracy:.1f}%")
        print(f"Average Time: {avg_time:.3f}s")
        print(f"Total Differences Found: {total_differences}")
        
        print(f"\n📊 Results by Type:")
        for result in successful_results:
            print(f"   - {result['test_name']}: {result['accuracy']:.1f}% accuracy, {result['differences']} differences")
    
    if successful_tests == total_tests:
        print(f"\n🎉 ALL COMPARISON TESTS PASSED!")
    else:
        print(f"\n⚠️  Some tests failed. Check details above.")

if __name__ == "__main__":
    asyncio.run(quick_comparison_test())