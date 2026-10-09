#!/usr/bin/env python3
"""
Get the exact API response structure
"""

import requests
import json

def check_response_structure():
    """Check exact API response structure"""
    
    url = "http://localhost:8000/api/comparison/compare"
    payload = {
        "file1_id": "2069a8fd-29e5-4ea6-bef9-13f4d256f356",
        "file2_id": "4f44347f-be05-4f1e-a2f3-1a5518c027fc",
        "comparison_options": {
            "exact_match": True,
            "ignore_formatting": True,
            "tolerance_settings": {}
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            
            print("🔍 Complete API Response Structure:")
            print(json.dumps(data, indent=2, default=str))
            
            print("\n📊 Data Structure Breakdown:")
            api_data = data.get('data', {})
            
            print(f"✅ Keys in data: {list(api_data.keys())}")
            
            # Check summary
            summary = api_data.get('summary', {})
            print(f"📈 Summary: {summary}")
            
            # Check differences
            detailed_diffs = api_data.get('detailed_differences', [])
            print(f"⚠️  Detailed differences count: {len(detailed_diffs)}")
            
            if detailed_diffs:
                print("First difference structure:")
                print(json.dumps(detailed_diffs[0], indent=2, default=str))
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    check_response_structure()