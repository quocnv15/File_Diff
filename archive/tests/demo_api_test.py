#!/usr/bin/env python3
"""
Demo test script for API endpoints
"""

import sys
import os
import json
import requests
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer demo_token"  # Mock token for demo
}


def test_health_endpoint():
    """Test health check endpoint"""
    print("🧪 Testing Health Check Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check successful")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            print(f"   Uptime: {data.get('uptime', 0)} seconds")
            
            if 'system_info' in data:
                sys_info = data['system_info']
                print(f"   CPU Usage: {sys_info.get('cpu_usage', 0)}%")
                print(f"   Memory Usage: {sys_info.get('memory_usage', 0)}%")
            
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the backend running?")
        print(f"   Expected URL: {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_root_endpoint():
    """Test root endpoint"""
    print("\n🧪 Testing Root Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint successful")
            print(f"   Message: {data.get('message', 'No message')}")
            print(f"   Version: {data.get('version', 'No version')}")
            print(f"   Docs URL: {data.get('docs_url', 'No docs URL')}")
            return True
        else:
            print(f"❌ Root endpoint failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Root endpoint test failed: {e}")
        return False


def test_supported_formats():
    """Test supported formats endpoint"""
    print("\n🧪 Testing Supported Formats Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/files/supported-formats", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Supported formats successful")
            
            if 'data' in data and 'input_formats' in data['data']:
                input_formats = data['data']['input_formats']
                print(f"   Supported input formats: {len(input_formats)}")
                
                for fmt in input_formats:
                    format_name = fmt.get('format', 'unknown')
                    extensions = fmt.get('extensions', [])
                    print(f"     - {format_name}: {', '.join(extensions)}")
            
            if 'data' in data and 'output_formats' in data['data']:
                output_formats = data['data']['output_formats']
                print(f"   Supported output formats: {len(output_formats)}")
                
                for fmt in output_formats:
                    format_name = fmt.get('format', 'unknown')
                    extensions = fmt.get('extensions', [])
                    print(f"     - {format_name}: {', '.join(extensions)}")
            
            return True
        else:
            print(f"❌ Supported formats failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Supported formats test failed: {e}")
        return False


def test_comparison_types():
    """Test comparison types endpoint"""
    print("\n🧪 Testing Comparison Types Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/comparison/comparison-types", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Comparison types successful")
            
            if 'data' in data:
                comparison_types = data['data']
                print(f"   Available comparison types: {len(comparison_types)}")
                
                for comp_type in comparison_types:
                    type_name = comp_type.get('type', 'unknown')
                    type_desc = comp_type.get('name', 'No description')
                    print(f"     - {type_name}: {type_desc}")
                    
                    if 'default_tolerances' in comp_type:
                        tolerances = comp_type['default_tolerances']
                        print(f"       Tolerances: {tolerances}")
            
            return True
        else:
            print(f"❌ Comparison types failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Comparison types test failed: {e}")
        return False


def test_file_validation():
    """Test file validation endpoint"""
    print("\n🧪 Testing File Validation Endpoint")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "Valid Excel file",
            "data": {
                "file_name": "test.xlsx",
                "file_size": 1024000,
                "file_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
        },
        {
            "name": "Valid CSV file",
            "data": {
                "file_name": "test.csv",
                "file_size": 512000,
                "file_type": "text/csv"
            }
        },
        {
            "name": "Invalid file type",
            "data": {
                "file_name": "test.txt",
                "file_size": 1024,
                "file_type": "text/plain"
            }
        },
        {
            "name": "File too large",
            "data": {
                "file_name": "huge.xlsx",
                "file_size": 100 * 1024 * 1024,  # 100MB
                "file_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }
        }
    ]
    
    all_passed = True
    
    for test_case in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/api/files/validate-file",
                json=test_case["data"],
                headers=HEADERS,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                is_valid = data.get('valid', False)
                expected_valid = test_case["name"].startswith("Valid")
                
                if is_valid == expected_valid:
                    print(f"   ✅ {test_case['name']}: Valid ({is_valid})")
                else:
                    print(f"   ⚠️  {test_case['name']}: Unexpected result ({is_valid})")
                    all_passed = False
                
                # Show validation details
                if 'validation_details' in data:
                    details = data['validation_details']
                    print(f"      File type supported: {details.get('file_type_supported', False)}")
                    print(f"      Size within limits: {details.get('size_within_limits', False)}")
                
                # Show warnings/errors
                if 'warnings' in data and data['warnings']:
                    print(f"      Warnings: {', '.join(data['warnings'])}")
                if 'errors' in data and data['errors']:
                    print(f"      Errors: {', '.join(data['errors'])}")
                    
            else:
                print(f"   ❌ {test_case['name']}: HTTP {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ {test_case['name']}: {e}")
            all_passed = False
    
    return all_passed


def test_error_handling():
    """Test error handling with invalid endpoints"""
    print("\n🧪 Testing Error Handling")
    print("=" * 50)
    
    error_test_cases = [
        {
            "name": "Non-existent endpoint",
            "method": "GET",
            "url": f"{BASE_URL}/api/nonexistent",
            "expected_status": 404
        },
        {
            "name": "Invalid file ID",
            "method": "GET", 
            "url": f"{BASE_URL}/api/files/invalid_file_id",
            "expected_status": 404
        },
        {
            "name": "Invalid comparison ID",
            "method": "GET",
            "url": f"{BASE_URL}/api/comparison/invalid_comparison_id",
            "expected_status": 404
        },
        {
            "name": "Invalid method on health endpoint",
            "method": "POST",
            "url": f"{BASE_URL}/api/health",
            "expected_status": [405, 422]  # Method Not Allowed or Unprocessable Entity
        }
    ]
    
    all_passed = True
    
    for test_case in error_test_cases:
        try:
            if test_case["method"] == "GET":
                response = requests.get(test_case["url"], timeout=5)
            elif test_case["method"] == "POST":
                response = requests.post(test_case["url"], json={}, timeout=5)
            
            expected_status = test_case["expected_status"]
            if isinstance(expected_status, list):
                status_match = response.status_code in expected_status
            else:
                status_match = response.status_code == expected_status
            
            if status_match:
                print(f"   ✅ {test_case['name']}: HTTP {response.status_code} (expected)")
            else:
                print(f"   ❌ {test_case['name']}: HTTP {response.status_code} (expected {expected_status})")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ {test_case['name']}: {e}")
            all_passed = False
    
    return all_passed


def test_response_times():
    """Test API response times"""
    print("\n🧪 Testing API Response Times")
    print("=" * 50)
    
    endpoints = [
        {"name": "Health Check", "url": f"{BASE_URL}/api/health"},
        {"name": "Root Endpoint", "url": f"{BASE_URL}/"},
        {"name": "Supported Formats", "url": f"{BASE_URL}/api/files/supported-formats"},
        {"name": "Comparison Types", "url": f"{BASE_URL}/api/comparison/comparison-types"}
    ]
    
    response_times = []
    
    for endpoint in endpoints:
        try:
            start_time = datetime.now()
            response = requests.get(endpoint["url"], timeout=5)
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds() * 1000  # Convert to ms
            
            if response.status_code == 200:
                print(f"   ✅ {endpoint['name']}: {response_time:.2f}ms")
                response_times.append(response_time)
            else:
                print(f"   ❌ {endpoint['name']}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {endpoint['name']}: {e}")
    
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        print(f"\n   📊 Response Time Statistics:")
        print(f"      Average: {avg_time:.2f}ms")
        print(f"      Min: {min_time:.2f}ms")
        print(f"      Max: {max_time:.2f}ms")
        
        # Performance assessment
        if avg_time < 100:
            print("   🚀 Excellent performance!")
        elif avg_time < 500:
            print("   ✅ Good performance!")
        elif avg_time < 1000:
            print("   ⚠️  Acceptable performance")
        else:
            print("   ❌ Poor performance - needs optimization")
    
    return len(response_times) > 0


def main():
    """Run all API demo tests"""
    print("🎯 File Diff Backend - API Demo Tests")
    print("=" * 60)
    print(f"🌐 Testing against: {BASE_URL}")
    print("📝 Note: Make sure the backend server is running!")
    print()
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
        ("Supported Formats", test_supported_formats),
        ("Comparison Types", test_comparison_types),
        ("File Validation", test_file_validation),
        ("Error Handling", test_error_handling),
        ("Response Times", test_response_times),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 API Demo Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API demo tests passed!")
        print("✨ API endpoints are working correctly!")
    else:
        print(f"⚠️  {total - passed} test(s) failed.")
        print("💡 Check if the backend server is running and accessible")
    
    print("\n💡 To start the backend server:")
    print("   cd backend")
    print("   python main.py")
    print("   # or: uvicorn app.main:app --reload")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)