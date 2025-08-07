#!/usr/bin/env python3
"""
Test script for the new frontend upload-and-analyze endpoint
"""

import requests
import numpy as np
from PIL import Image
import io
import json

def create_test_image():
    """Create a test image with some tumor-like features"""
    # Create a larger image similar to what might be uploaded
    img_array = np.ones((512, 512), dtype=np.uint8) * 120  # Gray background
    
    # Add some patterns to simulate brain-like structures
    img_array[100:300, 100:300] = 160  # Brain region
    img_array[150:200, 150:200] = 200  # Bright tumor-like region
    img_array[250:280, 250:280] = 80   # Dark region
    
    # Convert to PIL Image
    image = Image.fromarray(img_array, mode='L')
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_frontend_upload_and_analyze():
    """Test the new upload-and-analyze endpoint that frontend uses"""
    print("🔬 Testing frontend upload-and-analyze endpoint...")
    
    try:
        # Create test image
        image_data = create_test_image()
        print(f"✅ Created test image: {len(image_data)} bytes")
        
        # Prepare the request exactly like the frontend does
        files = {
            'mri_image': ('brain_scan.png', image_data, 'image/png')
        }
        data = {
            'user_id': 'test_user_123',
            'analysis_type': 'brain_tumor_detection'
        }
        
        url = 'http://localhost:8000/api/mri/upload-and-analyze'
        print(f"🌐 Sending request to: {url}")
        
        # Send request with proper form data
        response = requests.post(url, files=files, data=data, timeout=60)
        
        print(f"📊 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload-and-analyze test PASSED!")
            print(f"   Success: {result.get('success')}")
            
            if result.get('success'):
                analysis = result.get('analysis', {})
                print(f"   Image ID: {result.get('image_id')}")
                print(f"   Risk Level: {analysis.get('risk_level')}")
                print(f"   Overall Confidence: {analysis.get('overall_confidence')}")
                print(f"   Regions Found: {len(analysis.get('detected_regions', []))}")
                print(f"   Processing Time: {analysis.get('processing_time')}s")
                
                # Show detected regions if any
                detected_regions = analysis.get('detected_regions', [])
                if detected_regions:
                    print(f"   Detected Regions ({len(detected_regions)}):")
                    for i, region in enumerate(detected_regions[:3]):  # Show first 3
                        coords = region.get('coordinates', {})
                        print(f"     {i+1}. {region.get('type')} - confidence: {region.get('confidence'):.3f}")
                        print(f"        Location: {coords.get('x')},{coords.get('y')} ({coords.get('width')}x{coords.get('height')})")
                
                return True
            else:
                print(f"   Error: {result.get('error')}")
                return False
        else:
            print(f"❌ Upload-and-analyze test FAILED with status {response.status_code}")
            print(f"   Response text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload-and-analyze test ERROR: {e}")
        return False

def test_frontend_compatibility():
    """Test that the response format matches what frontend expects"""
    print("\n🎯 Testing frontend compatibility...")
    
    try:
        image_data = create_test_image()
        
        files = {
            'mri_image': ('test_scan.jpg', image_data, 'image/jpeg')
        }
        data = {
            'user_id': 'frontend_user',
            'analysis_type': 'brain_tumor_detection'
        }
        
        response = requests.post('http://localhost:8000/api/mri/upload-and-analyze', 
                               files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Check expected frontend fields
            expected_fields = ['success', 'image_id', 'analysis']
            missing_fields = [field for field in expected_fields if field not in result]
            
            if missing_fields:
                print(f"❌ Missing expected fields: {missing_fields}")
                return False
            
            if result.get('success'):
                analysis = result['analysis']
                expected_analysis_fields = ['detected_regions', 'overall_confidence', 'processing_time']
                missing_analysis_fields = [field for field in expected_analysis_fields if field not in analysis]
                
                if missing_analysis_fields:
                    print(f"❌ Missing analysis fields: {missing_analysis_fields}")
                    return False
                
                # Check detected_regions format
                regions = analysis.get('detected_regions', [])
                if regions:
                    region = regions[0]
                    expected_region_fields = ['id', 'type', 'confidence', 'coordinates', 'size_mm', 'location', 'risk_level']
                    missing_region_fields = [field for field in expected_region_fields if field not in region]
                    
                    if missing_region_fields:
                        print(f"❌ Missing region fields: {missing_region_fields}")
                        return False
                    
                    # Check coordinates structure
                    coords = region.get('coordinates', {})
                    expected_coord_fields = ['x', 'y', 'width', 'height']
                    missing_coord_fields = [field for field in expected_coord_fields if field not in coords]
                    
                    if missing_coord_fields:
                        print(f"❌ Missing coordinate fields: {missing_coord_fields}")
                        return False
                
                print("✅ Frontend compatibility test PASSED!")
                print(f"   All expected fields present")
                print(f"   Response structure matches frontend expectations")
                return True
            else:
                print("✅ Error response format is correct")
                return True
        else:
            print(f"❌ Compatibility test failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Compatibility test ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Frontend MRI Upload-and-Analyze Endpoint\n")
    
    # Test the main upload-and-analyze endpoint
    upload_success = test_frontend_upload_and_analyze()
    
    # Test frontend compatibility
    compatibility_success = test_frontend_compatibility()
    
    print(f"\n📈 Test Summary:")
    print(f"   Upload-and-analyze endpoint: {'✅ PASS' if upload_success else '❌ FAIL'}")
    print(f"   Frontend compatibility: {'✅ PASS' if compatibility_success else '❌ FAIL'}")
    
    if upload_success and compatibility_success:
        print(f"\n🎉 All frontend tests PASSED! The endpoint is ready for frontend integration.")
        print(f"🔗 Frontend can now use: POST /api/mri/upload-and-analyze")
    else:
        print(f"\n⚠️  Some tests failed - check the logs above for details.")
