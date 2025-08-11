#!/usr/bin/env python3
"""
Simple API endpoint test script to verify data requests endpoints
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'be'))

from fastapi.testclient import TestClient
from app.main import app

def test_endpoints():
    """Test all data requests endpoints"""
    client = TestClient(app)
    
    print("🔍 Testing Data Requests API Endpoints")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = client.get("/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health Check failed: {e}")
    
    # Test categories endpoint
    try:
        response = client.get("/api/v1/data-requests/categories")
        print(f"✅ Categories: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   Found {len(data.get('data', []))} categories")
                for cat in data.get('data', [])[:3]:  # Show first 3
                    print(f"   - {cat.get('name')}: {cat.get('description')}")
            else:
                print(f"   Response: {data}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Categories failed: {e}")
    
    # Test data requests list endpoint
    try:
        response = client.get("/api/v1/data-requests")
        print(f"✅ Data Requests List: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                requests_data = data.get('data', {})
                print(f"   Found {requests_data.get('total', 0)} total requests")
                print(f"   Page: {requests_data.get('page', 0)}, Limit: {requests_data.get('limit', 0)}")
                for req in requests_data.get('data', [])[:2]:  # Show first 2
                    print(f"   - {req.get('title')}")
            else:
                print(f"   Response: {data}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Data Requests List failed: {e}")
    
    # Test stats endpoint
    try:
        response = client.get("/api/v1/data-requests/stats")
        print(f"✅ Stats: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   Stats: {data.get('data')}")
            else:
                print(f"   Response: {data}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Stats failed: {e}")
        
    print("\n🔍 Testing Frontend API Service Alignment")
    print("=" * 50)
    
    # Compare frontend service endpoints with backend
    frontend_endpoints = [
        "GET /api/v1/data-requests",
        "GET /api/v1/data-requests/categories", 
        "POST /api/v1/data-requests",
        "GET /api/v1/data-requests/{id}",
        "PUT /api/v1/data-requests/{id}",
        "DELETE /api/v1/data-requests/{id}",
        "POST /api/v1/data-requests/{id}/vote",
        "DELETE /api/v1/data-requests/{id}/vote",
        "GET /api/v1/data-requests/popular",
        "GET /api/v1/data-requests/user",
        "GET /api/v1/data-requests/voted",
        "PUT /api/v1/data-requests/{id}/status"
    ]
    
    print("Frontend expects these endpoints:")
    for endpoint in frontend_endpoints:
        print(f"   {endpoint}")

if __name__ == "__main__":
    test_endpoints()