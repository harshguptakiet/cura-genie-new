#!/usr/bin/env python3
"""
Capture server logs to identify the exact error
"""

import subprocess
import sys
import time
import requests
import threading
from PIL import Image, ImageDraw

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (200, 200), color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    draw.ellipse([50, 50, 150, 150], fill=(100, 100, 100))
    draw.ellipse([90, 90, 110, 110], fill=(180, 180, 180))
    img.save("error_test.jpg")
    return "error_test.jpg"

def capture_server_output():
    """Start server and capture its output"""
    print("🚀 Starting server with output capture...")
    
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(8)
    
    # Test the failing endpoint
    print("\n🧪 Testing the failing endpoint...")
    test_image = create_test_image()
    
    try:
        with open(test_image, 'rb') as f:
            files = {'file': ('test.jpg', f, 'image/jpeg')}
            response = requests.post(
                "http://localhost:8000/api/mri/test-real-analysis", 
                files=files, 
                timeout=10
            )
        
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
    except Exception as e:
        print(f"Request error: {e}")
    
    # Give it a moment, then capture logs
    print("\n📋 Capturing server logs...")
    time.sleep(2)
    
    # Read available output
    try:
        stdout, stderr = process.communicate(timeout=1)
        print("\n📤 STDOUT:")
        print(stdout)
        print("\n📤 STDERR:")
        print(stderr)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print("\n📤 STDOUT (after kill):")
        print(stdout)
        print("\n📤 STDERR (after kill):")
        print(stderr)
    
    # Cleanup
    import os
    if os.path.exists(test_image):
        os.remove(test_image)

if __name__ == "__main__":
    capture_server_output()
