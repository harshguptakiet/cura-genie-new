#!/usr/bin/env python3
"""
MRI Upload Troubleshooting Guide
This script helps identify and fix common issues with MRI processing
"""

import os
import sys
import requests
import json
from PIL import Image
import io
import numpy as np

def create_test_brain_image():
    """Create a realistic test brain MRI image"""
    # Create a 256x256 grayscale medical image
    size = (256, 256)
    image_array = np.random.randint(20, 80, size=size, dtype=np.uint8)
    
    # Add brain-like circular structure
    center_x, center_y = size[0] // 2, size[1] // 2
    y, x = np.ogrid[:size[1], :size[0]]
    
    # Main brain area
    brain_radius = min(size) // 3
    brain_mask = (x - center_x)**2 + (y - center_y)**2 < brain_radius**2
    image_array[brain_mask] = np.random.randint(100, 150, np.sum(brain_mask))
    
    # Add some realistic brain structures
    # Ventricles (darker areas)
    ventricle_mask1 = (x - center_x + 20)**2 + (y - center_y - 10)**2 < 200
    ventricle_mask2 = (x - center_x - 20)**2 + (y - center_y - 10)**2 < 200
    image_array[ventricle_mask1] = np.random.randint(30, 60, np.sum(ventricle_mask1))
    image_array[ventricle_mask2] = np.random.randint(30, 60, np.sum(ventricle_mask2))
    
    # Add potential lesions (brighter spots)
    for i in range(2):
        lesion_x = center_x + np.random.randint(-60, 60)
        lesion_y = center_y + np.random.randint(-60, 60)
        lesion_size = np.random.randint(50, 200)
        lesion_mask = (x - lesion_x)**2 + (y - lesion_y)**2 < lesion_size
        image_array[lesion_mask] = np.random.randint(160, 220, np.sum(lesion_mask))
    
    # Convert to PIL Image
    image = Image.fromarray(image_array, mode='L')
    
    return image

def save_test_image(filename="test_brain_mri.png"):
    """Save a test brain MRI image"""
    image = create_test_brain_image()
    image.save(filename)
    print(f"✅ Created test brain MRI image: {filename}")
    return filename

def print_troubleshooting_steps():
    """Print comprehensive troubleshooting steps"""
    print("""
🔧 MRI PROCESSING TROUBLESHOOTING GUIDE
======================================

If you're seeing 'failed to process mri image please try again', here are the most common causes and solutions:

1. 🗄️  DATABASE ISSUES
   - Ensure database tables are created: `python -c "from db.database import create_tables; create_tables()"`
   - Check if MRIAnalysis table exists in your database
   - Verify database connection is working

2. 🔐 AUTHENTICATION PROBLEMS
   - Make sure you're logged in to the application
   - Check if your authentication token is valid
   - Verify the user exists in the users/auth tables

3. 📁 FILE SYSTEM ISSUES
   - Ensure uploads/mri directory exists and is writable
   - Check file permissions on the upload directory
   - Verify disk space is available

4. 🖼️  IMAGE FILE PROBLEMS
   - Use supported formats: JPG, PNG, TIFF, DICOM
   - Ensure image is not corrupted
   - Check image size (must be at least 50x50 pixels)
   - File size should be reasonable (not empty, not too large)

5. ⚙️  BACKGROUND PROCESSING ISSUES
   - Background tasks might not be running properly
   - Check if all required dependencies are installed
   - Verify Python environment has PIL, NumPy, etc.

6. 🔧 BACKEND SERVER ISSUES
   - Check if the backend server is running
   - Look at server logs for detailed error messages
   - Ensure all API endpoints are registered correctly

DEBUGGING STEPS:
================

1. Test the API endpoint:
   GET {base_url}/api/mri/test
   
2. Try the debug upload (without auth):
   POST {base_url}/api/mri/test-upload
   
3. Check analysis status:
   GET {base_url}/api/mri/debug/{{analysis_id}}
   
4. Look at server logs for detailed error messages

5. Check browser developer tools for network errors

MOST LIKELY CAUSES:
==================
1. Background task failed due to missing dependencies
2. Database table not created properly  
3. Authentication token expired/invalid
4. File upload timeout or size limits
5. Server configuration issues

TRY THIS FIRST:
===============
1. Restart the backend server
2. Clear browser cache and cookies
3. Try a different image file (use the generated test image)
4. Check browser developer console for errors
5. Look at backend server logs
    """)

def generate_curl_commands():
    """Generate curl commands for testing"""
    print("""
🔍 DEBUGGING WITH CURL COMMANDS
===============================

1. Test API availability:
   curl -X GET "http://localhost:8000/api/mri/test"

2. Test image upload without authentication:
   curl -X POST "http://localhost:8000/api/mri/test-upload" \\
        -F "file=@test_brain_mri.png"

3. Test with authentication (replace YOUR_TOKEN):
   curl -X POST "http://localhost:8000/api/mri/upload" \\
        -H "Authorization: Bearer YOUR_TOKEN" \\
        -F "file=@test_brain_mri.png"

4. Check analysis status:
   curl -X GET "http://localhost:8000/api/mri/debug/1" \\
        -H "Authorization: Bearer YOUR_TOKEN"
    """)

def check_server_status(base_url="http://localhost:8000"):
    """Check if the server is running and MRI endpoints are available"""
    print(f"🔍 Checking server status at {base_url}...")
    
    try:
        # Test main server
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Main server is running")
        else:
            print(f"   ⚠️  Server responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Cannot connect to server: {e}")
        return False
    
    try:
        # Test MRI API endpoint
        response = requests.get(f"{base_url}/api/mri/test", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("   ✅ MRI API is available")
            print(f"   📁 Upload directory: {data.get('upload_dir')}")
            print(f"   📂 Directory exists: {data.get('directory_exists')}")
            print(f"   ✏️  Directory writable: {data.get('directory_writable')}")
            return True
        else:
            print(f"   ❌ MRI API responded with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Cannot connect to MRI API: {e}")
        return False

def test_upload_without_auth(base_url="http://localhost:8000", image_file="test_brain_mri.png"):
    """Test upload without authentication for debugging"""
    print(f"🧪 Testing upload without authentication...")
    
    if not os.path.exists(image_file):
        print(f"   ❌ Test image file {image_file} not found")
        return False
    
    try:
        with open(image_file, 'rb') as f:
            files = {'file': (image_file, f, 'image/png')}
            response = requests.post(
                f"{base_url}/api/mri/test-upload", 
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("   ✅ Test upload successful!")
                print(f"   📊 File info: {data.get('file_info')}")
                print(f"   🖼️  Image info: {data.get('image_info')}")
                return True
            else:
                print(f"   ❌ Test upload failed: {data.get('error')}")
                return False
        else:
            print(f"   ❌ Upload failed with status {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
        return False

def main():
    """Main troubleshooting function"""
    print("🚨 MRI PROCESSING TROUBLESHOOTING")
    print("=" * 50)
    
    # Create test image
    test_image = save_test_image()
    
    # Check server status
    server_ok = check_server_status()
    
    if server_ok:
        # Test upload without auth
        test_upload_without_auth(image_file=test_image)
    
    # Print troubleshooting guide
    print_troubleshooting_steps()
    
    # Generate debugging commands
    generate_curl_commands()
    
    print("\n" + "=" * 50)
    print("💡 NEXT STEPS:")
    print("1. Use the generated test_brain_mri.png image for testing")
    print("2. Check the server logs for detailed error messages")
    print("3. Try the curl commands above to isolate the issue")
    print("4. If all tests pass but the UI still fails, check browser console")
    print("5. Consider restarting the backend server")

if __name__ == "__main__":
    main()
