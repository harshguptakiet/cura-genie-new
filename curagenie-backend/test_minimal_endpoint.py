#!/usr/bin/env python3
"""
Test script for the minimal endpoint to isolate issues
"""

import requests
import numpy as np
from PIL import Image
import io
import json

def create_simple_test_image():
    """Create a simple test image"""
    # Create a simple grayscale image with some patterns
    img_array = np.ones((256, 256), dtype=np.uint8) * 128  # Gray background
    
    # Add some patterns to simulate brain-like structures
    img_array[50:150, 50:150] = 180  # Brighter region
    img_array[80:120, 80:120] = 100  # Darker region inside
    
    # Convert to PIL Image
    image = Image.fromarray(img_array, mode='L')
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_minimal_endpoint():
    """Test the minimal endpoint"""
    print("🧪 Testing minimal endpoint...")
    
    try:
        # Create test image
        image_data = create_simple_test_image()
        print(f"✅ Created test image: {len(image_data)} bytes")
        
        # Prepare the request
        files = {
            'file': ('test_image.png', image_data, 'image/png')
        }
        
        url = 'http://localhost:8000/api/mri/minimal-test'
        print(f"🌐 Sending request to: {url}")
        
        # Send request
        response = requests.post(url, files=files, timeout=30)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Minimal test PASSED!")
            print(f"   Result: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Minimal test FAILED with status {response.status_code}")
            print(f"   Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Minimal test ERROR: {e}")
        return False

def test_real_analysis_endpoint():
    """Test the real analysis endpoint"""
    print("\n🔬 Testing real analysis endpoint...")
    
    try:
        # Create test image
        image_data = create_simple_test_image()
        print(f"✅ Created test image: {len(image_data)} bytes")
        
        # Prepare the request
        files = {
            'file': ('test_brain_scan.png', image_data, 'image/png')
        }
        
        url = 'http://localhost:8000/api/mri/test-real-analysis'
        print(f"🌐 Sending request to: {url}")
        
        # Send request
        response = requests.post(url, files=files, timeout=60)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Real analysis test PASSED!")
            print(f"   Success: {result.get('success')}")
            if result.get('success'):
                analysis_result = result.get('analysis_result', {})
                print(f"   Status: {analysis_result.get('status')}")
                print(f"   Method: {analysis_result.get('method')}")
                print(f"   Regions detected: {analysis_result.get('overall_assessment', {}).get('num_regions_detected', 0)}")
                print(f"   Risk level: {analysis_result.get('overall_assessment', {}).get('risk_level')}")
            else:
                print(f"   Error: {result.get('error')}")
            return True
        else:
            print(f"❌ Real analysis test FAILED with status {response.status_code}")
            print(f"   Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Real analysis test ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting endpoint testing...\n")
    
    # Test minimal endpoint first
    minimal_success = test_minimal_endpoint()
    
    # If minimal works, test real analysis
    if minimal_success:
        real_success = test_real_analysis_endpoint()
    else:
        print("\n⚠️  Skipping real analysis test since minimal test failed")
        real_success = False
    
    print(f"\n📈 Test Summary:")
    print(f"   Minimal endpoint: {'✅ PASS' if minimal_success else '❌ FAIL'}")
    print(f"   Real analysis endpoint: {'✅ PASS' if real_success else '❌ FAIL'}")
    
    if minimal_success and real_success:
        print("\n🎉 All tests PASSED! The endpoints are working correctly.")
    elif minimal_success:
        print("\n🤔 Minimal test passed but real analysis failed - issue is in the analysis logic.")
    else:
        print("\n💥 Basic endpoint test failed - there's a fundamental issue with the API.")
