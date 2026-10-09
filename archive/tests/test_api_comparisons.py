#!/usr/bin/env python3
"""
Test comparison functionality via API endpoints
"""

import os
import sys
import time
from pathlib import Path

# Add backend directory to path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)

from fastapi.testclient import TestClient
from backend.app.main import app

class APIComparisonTestRunner:
    """Test runner for API-based file comparisons"""
    
    def __init__(self):
        self.client = TestClient(app)
        self.samples_dir = Path.cwd() / 'samples'
        self.uploaded_files = {}  # Store file_id for uploaded files
        self.results = []
    
    async def upload_file(self, file_path: Path):
        """Upload a file and return file_id"""
        if not file_path.exists():
            return None
            
        try:
            with open(file_path, 'rb') as f:
                # Determine content type
                ext = file_path.suffix.lower()
                content_types = {
                    '.csv': 'text/csv',
                    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    '.xls': 'application/vnd.ms-excel',
                    '.pdf': 'application/pdf'
                }
                content_type = content_types.get(ext, 'application/octet-stream')
                
                files = {'file': (file_path.name, f, content_type)}
                response = self.client.post('/api/files/upload', files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    file_id = result['data']['file_id']
                    
                    # Process the file
                    process_response = self.client.post(f'/api/files/{file_id}/process')
                    if process_response.status_code == 200:
                        process_result = process_response.json()
                        return file_id
                    else:
                        print(f"❌ Failed to process {file_path.name}: {process_response.text}")
                        return None
                else:
                    print(f"❌ Failed to upload {file_path.name}: {response.text}")
                    return None
                    
        except Exception as e:
            print(f"❌ Error uploading {file_path.name}: {e}")
            return None
    
    async def prepare_files(self):
        """Upload and process all needed files"""
        print("📤 Preparing files for API comparison tests...")
        
        files_to_prepare = [
            'product_comparisons/product_comparison_v1.csv',
            'product_comparisons/product_comparison_v2.csv',
            'product_comparisons/product_comparison_v1.xlsx',
            'product_comparisons/product_comparison_v2.xlsx',
            'product_comparisons/product_comparison_v1.pdf',
            'product_comparisons/product_comparison_v2.pdf',
            'invoice_comparisons/invoice_001.csv',
            'invoice_comparisons/invoice_002.csv',
            'invoice_comparisons/invoice_001.xlsx',
            'invoice_comparisons/invoice_002.xlsx',
        ]
        
        for file_name in files_to_prepare:
            file_path = self.samples_dir / file_name
            file_id = await self.upload_file(file_path)
            if file_id:
                self.uploaded_files[file_name] = file_id
                print(f"   ✅ {file_name} -> {file_id}")
            else:
                print(f"   ❌ {file_name} -> Failed")
    
    async def test_api_comparison(self, file1_key: str, file2_key: str, test_name: str, options=None):
        """Test comparison via API"""
        if file1_key not in self.uploaded_files or file2_key not in self.uploaded_files:
            return {
                'test_name': test_name,
                'success': False,
                'error': 'Files not uploaded or processed'
            }
        
        try:
            file1_id = self.uploaded_files[file1_key]
            file2_id = self.uploaded_files[file2_key]
            
            # Prepare comparison data
            comparison_data = {
                'file1_id': file1_id,
                'file2_id': file2_id,
                'options': options or {
                    'comparison_type': 'products',
                    'exact_match': False,
                    'tolerance_settings': {
                        'quantity': 0.1,
                        'unit_price': 0.01,
                        'amount': 0.01
                    }
                }
            }
            
            start_time = time.time()
            response = self.client.post('/api/comparison/compare', json=comparison_data)
            comparison_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get('summary', {})
                differences = result.get('differences', [])
                
                return {
                    'test_name': test_name,
                    'success': True,
                    'comparison_time': comparison_time,
                    'total_rows': summary.get('total_rows_compared', 0),
                    'matching_rows': summary.get('matching_rows', 0),
                    'different_rows': summary.get('different_rows', 0),
                    'accuracy_rate': summary.get('accuracy_rate', 0),
                    'differences_found': len(differences),
                    'file1_type': Path(file1_key).suffix.upper(),
                    'file2_type': Path(file2_key).suffix.upper(),
                    'error': None
                }
            else:
                return {
                    'test_name': test_name,
                    'success': False,
                    'error': f'API Error: {response.status_code} - {response.text}'
                }
                
        except Exception as e:
            return {
                'test_name': test_name,
                'success': False,
                'error': str(e)
            }
    
    async def test_same_format_api_comparisons(self):
        """Test API comparisons between same file formats"""
        print("\n🔄 Testing API Same Format Comparisons")
        print("=" * 50)
        
        test_scenarios = [
            # CSV comparisons
            ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v2.csv', 'API CSV Product Comparison'),
            ('invoice_comparisons/invoice_001.csv', 'invoice_comparisons/invoice_002.csv', 'API CSV Invoice Comparison'),
            
            # Excel comparisons
            ('product_comparisons/product_comparison_v1.xlsx', 'product_comparisons/product_comparison_v2.xlsx', 'API Excel Product Comparison'),
            ('invoice_comparisons/invoice_001.xlsx', 'invoice_comparisons/invoice_002.xlsx', 'API Excel Invoice Comparison'),
        ]
        
        for file1, file2, test_name in test_scenarios:
            result = await self.test_api_comparison(file1, file2, test_name)
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Format: {result['file1_type']} vs {result['file2_type']}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    async def test_cross_format_api_comparisons(self):
        """Test API comparisons between different file formats"""
        print("\n🔄 Testing API Cross-Format Comparisons")
        print("=" * 50)
        
        test_scenarios = [
            # CSV vs Excel
            ('product_comparisons/product_comparison_v1.csv', 'product_comparisons/product_comparison_v1.xlsx', 'API CSV vs Excel (v1)'),
            ('product_comparisons/product_comparison_v2.csv', 'product_comparisons/product_comparison_v2.xlsx', 'API CSV vs Excel (v2)'),
        ]
        
        for file1, file2, test_name in test_scenarios:
            result = await self.test_api_comparison(file1, file2, test_name)
            self.results.append(result)
            
            if result['success']:
                print(f"   ✅ {result['test_name']}")
                print(f"      - Format: {result['file1_type']} vs {result['file2_type']}")
                print(f"      - Rows compared: {result['total_rows']}")
                print(f"      - Differences: {result['differences_found']}")
                print(f"      - Accuracy: {result['accuracy_rate']:.1f}%")
                print(f"      - Time: {result['comparison_time']:.3f}s")
            else:
                print(f"   ❌ {result['test_name']} - {result['error']}")
    
    def print_summary(self):
        """Print API comparison test summary"""
        print(f"\n{'='*80}")
        print(f"📊 API COMPARISON TEST SUMMARY")
        print(f"{'='*80}")
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"Total API Comparison Tests: {total_tests}")
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
            print(f"Average API Comparison Time: {avg_time:.3f}s")
            print(f"Average Accuracy: {avg_accuracy:.1f}%")
        
        # Show failed tests
        failed_results = [r for r in self.results if not r['success']]
        if failed_results:
            print(f"\n❌ Failed API Tests:")
            for result in failed_results:
                print(f"   - {result['test_name']}: {result['error']}")
        
        if failed_tests == 0:
            print(f"\n🎉 ALL API COMPARISON TESTS PASSED!")
        elif successful_tests / total_tests >= 0.8:
            print(f"\n✅ GOOD PERFORMANCE! Most API comparison tests passed.")
        else:
            print(f"\n⚠️  Some API comparison issues detected.")
        
        print(f"{'='*80}")
    
    async def run_all_tests(self):
        """Run all API comparison tests"""
        print("🚀 Starting API File Comparison Tests")
        print(f"Testing files from: {self.samples_dir}")
        
        start_time = time.time()
        
        # Prepare files first
        await self.prepare_files()
        
        if len(self.uploaded_files) < 2:
            print(f"\n❌ Not enough files uploaded for comparison tests. Got {len(self.uploaded_files)} files.")
            return
        
        # Run comparison tests
        await self.test_same_format_api_comparisons()
        await self.test_cross_format_api_comparisons()
        
        total_time = time.time() - start_time
        print(f"\n⏱️  Total test execution time: {total_time:.2f} seconds")
        self.print_summary()

async def main():
    """Main function"""
    runner = APIComparisonTestRunner()
    await runner.run_all_tests()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())