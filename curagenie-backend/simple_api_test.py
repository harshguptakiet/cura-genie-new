#!/usr/bin/env python3
"""
Simple API test to isolate the issue
"""

import requests
import os
from PIL import Image, ImageDraw
import time
import subprocess
import sys

def create_minimal_test_image():
    """Create minimal test image"""
    img = Image.new('RGB', (200, 200), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    draw.ellipse([50, 50, 150, 150], fill=(100, 100, 100))
    draw.ellipse([90, 90, 110, 110], fill=(180, 180, 180))  # Bright spot
    img.save("minimal_test.jpg")
    return "minimal_test.jpg"

def start_server():
    """Start server and wait for it to be ready"""
    print("Starting server...")
    server_process = subprocess.Popen([sys.executable, "main.py"], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)
    
    # Wait for server to start
    for i in range(20):
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return server_process
        except:
            time.sleep(1)
            print(f"Waiting... ({i+1}/20)")
    
    print("❌ Server failed to start")
    server_process.terminate()
    return None

def test_simple_mri_api():
    """Test with minimal API calls"""
    server_process = start_server()
    if not server_process:
        return False
    
    try:
        # Test 1: Basic health
        print("\n1. Testing basic health...")
        response = requests.get("http://localhost:8000/health")
        print(f"Health: {response.status_code}")
        
        # Test 2: MRI API test endpoint
        print("\n2. Testing MRI API...")
        response = requests.get("http://localhost:8000/api/mri/test")
        print(f"MRI test: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        
        # Test 3: Simple file upload test
        print("\n3. Testing simple file upload...")
        test_image = create_minimal_test_image()
        
        try:
            with open(test_image, 'rb') as f:
                files = {'file': ('test.jpg', f, 'image/jpeg')}
                response = requests.post("http://localhost:8000/api/mri/test-upload", 
                                       files=files, timeout=10)
            
            print(f"Upload test: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Upload success: {data.get('success', False)}")
            else:
                print(f"Upload error: {response.text}")
                
        except Exception as e:
            print(f"Upload test error: {e}")
        
        # Test 4: Real analysis test (the problematic one)
        print("\n4. Testing real analysis (this is the failing one)...")
        try:
            with open(test_image, 'rb') as f:
                files = {'file': ('test.jpg', f, 'image/jpeg')}
                print("Sending request...")
                response = requests.post("http://localhost:8000/api/mri/test-real-analysis", 
                                       files=files, timeout=15)
            
            print(f"Real analysis: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Analysis success: {data.get('success', False)}")
                if not data.get('success'):
                    print(f"Analysis error: {data.get('error')}")
            else:
                print(f"Analysis failed: {response.text}")
                
        except Exception as e:
            print(f"Real analysis error: {e}")
        
        return True
        
    finally:
        print("\nStopping server...")
        server_process.terminate()
        server_process.wait()
        
        # Cleanup
        if os.path.exists("minimal_test.jpg"):
            os.remove("minimal_test.jpg")

if __name__ == "__main__":
    print("🧪 Simple API Test")
    test_simple_mri_api()
