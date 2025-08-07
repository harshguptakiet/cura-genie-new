#!/usr/bin/env python3
"""
Test Backend APIs Live
"""

import requests
import time
import threading
import subprocess
import sys
from pathlib import Path

def start_backend_server():
    """Start backend server in background"""
    try:
        process = subprocess.Popen([
            sys.executable, "test_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for server to start
        time.sleep(5)
        return process
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def test_api_endpoints():
    """Test all backend API endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    tests = [
        ("Root endpoint", "/"),
        ("Health check", "/health"),
        ("WebSocket status", "/ws/status"),
        ("API Documentation", "/docs"),
    ]
    
    print("🌐 Testing Backend API Endpoints...")
    results = []
    
    for test_name, endpoint in tests:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {test_name}: Working ({response.status_code})")
                if endpoint == "/":
                    data = response.json()
                    print(f"      Message: {data.get('message', 'N/A')}")
                elif endpoint == "/health":
                    data = response.json()
                    print(f"      Status: {data.get('status', 'N/A')}")
                results.append(True)
            else:
                print(f"   ⚠️  {test_name}: Status {response.status_code}")
                results.append(False)
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {test_name}: Connection failed (server not running?)")
            results.append(False)
        except Exception as e:
            print(f"   ❌ {test_name}: Error - {e}")
            results.append(False)
    
    return results

def test_ml_endpoints():
    """Test ML prediction endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("\n🧠 Testing ML API Endpoints...")
    
    # Test ML prediction endpoint
    try:
        payload = {
            "user_id": "test_user_123",
            "clinical_data": {
                "age": 45,
                "bmi": 28.5,
                "glucose_level": 140,
                "blood_pressure": 130
            }
        }
        
        response = requests.post(f"{base_url}/api/ml/trigger-prediction", json=payload, timeout=10)
        if response.status_code == 202:
            print("   ✅ ML Prediction: Started successfully")
            data = response.json()
            print(f"      Status: {data.get('status')}")
            print(f"      User ID: {data.get('user_id')}")
        else:
            print(f"   ⚠️  ML Prediction: Status {response.status_code}")
            print(f"      Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ ML Prediction: Error - {e}")

def test_genomic_endpoints():
    """Test genomic analysis endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("\n🧬 Testing Genomic API Endpoints...")
    
    # Test genomic data listing
    try:
        response = requests.get(f"{base_url}/api/genomic/data/test_user", timeout=10)
        if response.status_code == 200:
            print("   ✅ Genomic Data List: Working")
            data = response.json()
            print(f"      Found {len(data)} genomic files")
        else:
            print(f"   ⚠️  Genomic Data List: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Genomic Data List: Error - {e}")

def main():
    print("🚀 CuraGenie Backend Live Test")
    print("=" * 50)
    
    # Start backend
    print("🏃‍♂️ Starting backend server...")
    backend = start_backend_server()
    
    if not backend:
        print("❌ Cannot start backend server")
        return
    
    try:
        # Test basic endpoints
        api_results = test_api_endpoints()
        
        if any(api_results):
            # Test ML endpoints
            test_ml_endpoints()
            
            # Test genomic endpoints  
            test_genomic_endpoints()
            
            # Summary
            print("\n" + "=" * 50)
            print("📊 BACKEND TEST SUMMARY")
            print("=" * 50)
            
            passed = sum(api_results)
            total = len(api_results)
            
            print(f"✅ Basic APIs: {passed}/{total} working")
            
            if passed >= 3:
                print("🎉 BACKEND IS WORKING GREAT!")
                print(f"🌐 Access your API at: http://127.0.0.1:8000")
                print(f"📖 Documentation at: http://127.0.0.1:8000/docs")
                print("\n💡 Next: Install Node.js to test frontend")
            else:
                print("⚠️  Some issues detected")
        
        else:
            print("❌ Backend server not responding")
    
    finally:
        # Cleanup
        if backend:
            print(f"\n🛑 Stopping backend server...")
            backend.terminate()
            backend.wait()
            print("✅ Backend stopped")

if __name__ == "__main__":
    main()
