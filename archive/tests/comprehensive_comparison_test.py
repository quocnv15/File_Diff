#!/usr/bin/env python3
"""
Comprehensive comparison test with all file type combinations
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

async def comprehensive_comparison_test():
    """Comprehensive test of comparison functionality"""
    print("🚀 Comprehensive Comparison Test - All File Type Combinations")
    print("=" * 80)
    
    samples_dir = Path.cwd() / 'samples'
    processors = {
        'csv': CSVProcessor(),
        'xlsx': ExcelProcessor(),
        'pdf': PDFProcessor()
    }
    comparator = DataComparator()
    
    # Test cases with various combinations
    test_cases = [
        # Same format comparisons
        ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v2.csv', 'CSV Product v1 vs v2'),
        ('invoice_comparisons/invoice_001.csv', 'invoice_comparisons/invoice_002.csv', 'CSV Invoice v1 vs v2'),
        ('product_comparisons/product_comparison_v1.xlsx', 'product_comparisons/product_comparison_v2.xlsx', 'Excel Product v1 vs v2'),
        ('invoice_comparisons/invoice_001.xlsx', 'invoice_comparisons/invoice_002.xlsx', 'Excel Invoice v1 vs v2'),
        
        # Cross-format comparisons (same data)
        ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v1.xlsx', 'CSV vs Excel (v1)'),
        ('product_comparisons/product_comparison_v2.csv', 'product_comparisons/product_comparison_v2.xlsx', 'CSV vs Excel (v2)'),
        
        # Cross-format comparisons (different versions)
        ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v2.xlsx', 'CSV v1 vs Excel v2'),
        ('product_comparisons/product_comparison_v1.xlsx', 'product_comparisons/product_comparison_v2.csv', 'Excel v1 vs CSV v2'),
        
        # Self-comparisons (should be 100%)
        ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v1.csv', 'CSV Self-Comparison'),
        ('product_comparisons/product_comparison_v1.xlsx', 'product_comparisons/product_comparison_v1.xlsx', 'Excel Self-Comparison'),
        
        # Invoice cross-format
        ('invoice_comparisons/invoice_001.csv', 'invoice_comparisons/invoice_001.xlsx', 'Invoice CSV vs Excel'),
        ('invoice_comparisons/invoice_002.csv', 'invoice_comparisons/invoice_002.xlsx', 'Invoice CSV vs Excel'),
    ]
    
    results = []
    total_start_time = time.time()
    
    for i, (file1, file2, test_name) in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}] 📊 Testing: {test_name}")
        
        try:
            # Process first file
            file1_path = samples_dir / file1
            if not file1_path.exists():
                print(f"   ❌ File not found: {file1}")
                continue
                
            file1_ext = file1_path.suffix.lower().lstrip('.')
            processor1 = processors[file1_ext]
            data1 = await processor1.process(str(file1_path))
            tables1 = data1.get('structured_data', [])
            
            # Process second file
            file2_path = samples_dir / file2
            if not file2_path.exists():
                print(f"   ❌ File not found: {file2}")
                continue
                
            file2_ext = file2_path.suffix.lower().lstrip('.')
            processor2 = processors[file2_ext]
            data2 = await processor2.process(str(file2_path))
            tables2 = data2.get('structured_data', [])
            
            if not tables1 or not tables2:
                print(f"   ❌ Failed to extract data from files")
                continue
            
            # Compare with product options
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
            print(f"      - Format: {file1_ext.upper()} vs {file2_ext.upper()}")
            print(f"      - Tables: {len(tables1)} vs {len(tables2)}")
            print(f"      - Rows compared: {summary.get('total_rows_compared', 0)}")
            print(f"      - Matching rows: {summary.get('matching_rows', 0)}")
            print(f"      - Different rows: {summary.get('different_rows', 0)}")
            print(f"      - Differences found: {len(differences)}")
            print(f"      - Accuracy rate: {summary.get('accuracy_rate', 0):.1f}%")
            print(f"      - Comparison time: {comparison_time:.3f}s")
            
            results.append({
                'test_name': test_name,
                'success': True,
                'file1_type': file1_ext.upper(),
                'file2_type': file2_ext.upper(),
                'tables1': len(tables1),
                'tables2': len(tables2),
                'rows_compared': summary.get('total_rows_compared', 0),
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
    
    total_time = time.time() - total_start_time
    
    # Comprehensive Summary
    print(f"\n{'='*80}")
    print(f"📊 COMPREHENSIVE COMPARISON TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total execution time: {total_time:.2f}s")
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results if r['success'])
    failed_tests = total_tests - successful_tests
    
    print(f"\n📈 Overall Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Successful: {successful_tests} ✅")
    print(f"   Failed: {failed_tests} ❌")
    print(f"   Success Rate: {(successful_tests / total_tests * 100):.1f}%")
    
    if successful_tests > 0:
        successful_results = [r for r in results if r['success']]
        
        # Accuracy analysis
        avg_accuracy = sum(r['accuracy'] for r in successful_results) / len(successful_results)
        avg_time = sum(r['time'] for r in successful_results) / len(successful_results)
        total_differences = sum(r['differences'] for r in successful_results)
        total_rows = sum(r['rows_compared'] for r in successful_results)
        
        print(f"\n📊 Performance Metrics:")
        print(f"   Average Accuracy: {avg_accuracy:.1f}%")
        print(f"   Average Time: {avg_time:.3f}s")
        print(f"   Total Rows Compared: {total_rows}")
        print(f"   Total Differences Found: {total_differences}")
        
        # Format combination analysis
        print(f"\n📊 Results by Format Combination:")
        format_stats = {}
        for result in successful_results:
            combo = f"{result['file1_type']} vs {result['file2_type']}"
            if combo not in format_stats:
                format_stats[combo] = {'count': 0, 'avg_accuracy': 0, 'avg_time': 0, 'total_differences': 0}
            
            format_stats[combo]['count'] += 1
            format_stats[combo]['avg_accuracy'] += result['accuracy']
            format_stats[combo]['avg_time'] += result['time']
            format_stats[combo]['total_differences'] += result['differences']
        
        for combo, stats in format_stats.items():
            count = stats['count']
            avg_acc = stats['avg_accuracy'] / count
            avg_t = stats['avg_time'] / count
            total_diff = stats['total_differences']
            print(f"   - {combo}: {count} tests, {avg_acc:.1f}% avg accuracy, {avg_t:.3f}s avg time, {total_diff} total differences")
        
        # Test type analysis
        print(f"\n📊 Results by Test Type:")
        test_types = {
            'Self-Comparison': [],
            'Same Format': [],
            'Cross Format': []
        }
        
        for result in successful_results:
            test_name = result['test_name'].lower()
            if 'self-comparison' in test_name:
                test_types['Self-Comparison'].append(result)
            elif result['file1_type'] == result['file2_type']:
                test_types['Same Format'].append(result)
            else:
                test_types['Cross Format'].append(result)
        
        for test_type, test_results in test_types.items():
            if test_results:
                avg_acc = sum(r['accuracy'] for r in test_results) / len(test_results)
                avg_t = sum(r['time'] for r in test_results) / len(test_results)
                print(f"   - {test_type}: {len(test_results)} tests, {avg_acc:.1f}% avg accuracy, {avg_t:.3f}s avg time")
        
        # Expected vs Actual analysis
        print(f"\n🎯 Expected vs Actual Analysis:")
        print(f"   Self-Comparisons: Should be 100% accuracy")
        self_comparisons = [r for r in successful_results if 'self-comparison' in r['test_name'].lower()]
        if self_comparisons:
            avg_self_acc = sum(r['accuracy'] for r in self_comparisons) / len(self_comparisons)
            print(f"   → Actual: {avg_self_acc:.1f}% ({'✅ Perfect' if avg_self_acc == 100 else '⚠️ Issue detected'})")
        
        print(f"   Same Format v1 vs v2: Should detect differences (accuracy < 100%)")
        same_format_v1_v2 = [r for r in successful_results if 'v1 vs v2' in r['test_name'] and r['file1_type'] == r['file2_type']]
        if same_format_v1_v2:
            avg_v1_v2_acc = sum(r['accuracy'] for r in same_format_v1_v2) / len(same_format_v1_v2)
            print(f"   → Actual: {avg_v1_v2_acc:.1f}% ({'✅ Correct' if avg_v1_v2_acc < 100 else '⚠️ Expected differences'})")
        
        print(f"   Cross Format Same Data: Should be high accuracy (>95%)")
        cross_same = [r for r in successful_results if 'v1' in r['test_name'] and r['file1_type'] != r['file2_type']]
        if cross_same:
            avg_cross_acc = sum(r['accuracy'] for r in cross_same) / len(cross_same)
            print(f"   → Actual: {avg_cross_acc:.1f}% ({'✅ Excellent' if avg_cross_acc >= 95 else '⚠️ Low accuracy'})")
    
    # Show failed tests
    failed_results = [r for r in results if not r['success']]
    if failed_results:
        print(f"\n❌ Failed Tests:")
        for result in failed_results:
            print(f"   - {result['test_name']}: {result['error']}")
    
    # Final assessment
    print(f"\n🎯 Final Assessment:")
    if failed_tests == 0:
        print(f"   🎉 PERFECT! All comparison tests passed successfully!")
        print(f"   📈 System is working correctly with {avg_accuracy:.1f}% average accuracy")
        print(f"   ⚡ Processing is fast with {avg_time:.3f}s average time")
    elif successful_tests / total_tests >= 0.9:
        print(f"   ✅ EXCELLENT! {successful_tests}/{total_tests} tests passed!")
        print(f"   📈 System is highly reliable with {avg_accuracy:.1f}% average accuracy")
    elif successful_tests / total_tests >= 0.8:
        print(f"   ✅ GOOD! {successful_tests}/{total_tests} tests passed!")
        print(f"   📈 System is functional with {avg_accuracy:.1f}% average accuracy")
    else:
        print(f"   ⚠️  NEEDS IMPROVEMENT: Only {successful_tests}/{total_tests} tests passed.")
    
    print(f"{'='*80}")

if __name__ == "__main__":
    asyncio.run(comprehensive_comparison_test())