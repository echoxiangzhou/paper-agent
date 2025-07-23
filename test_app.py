#!/usr/bin/env python3
"""
Test script for FastAPI application
"""

import sys
import os

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def test_app_import():
    """Test that the FastAPI app can be imported successfully."""
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
        print(f"📝 App title: {app.title}")
        print(f"🔧 Environment: {app.extra.get('environment', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ Failed to import app: {e}")
        return False

def test_health_endpoint():
    """Test the health endpoint."""
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/health")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working")
            print(f"📊 Response: {data}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Paper Agent Backend...")
    print("=" * 50)
    
    success = True
    
    # Test app import
    success &= test_app_import()
    print()
    
    # Test health endpoint
    success &= test_health_endpoint()
    print()
    
    if success:
        print("🎉 All tests passed! Backend is ready.")
    else:
        print("💥 Some tests failed. Check the errors above.")
        sys.exit(1)