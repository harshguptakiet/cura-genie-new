#!/usr/bin/env python3
"""
Test script for MRI processing functionality
This will help diagnose any issues with the MRI analysis pipeline
"""

import os
import sys
import io
from PIL import Image
import numpy as np
import json
from datetime import datetime

# Add the current directory to Python path so we can import modules
sys.path.append('.')

def create_test_image(size=(500, 500), format='PNG'):
    """Create a test medical-looking image"""
    # Create a grayscale medical-looking image
    image_array = np.random.randint(50, 200, size=(size[1], size[0]), dtype=np.uint8)
    
    # Add some circular structures to mimic brain anatomy
    center_x, center_y = size[0] // 2, size[1] // 2
    y, x = np.ogrid[:size[1], :size[0]]
    
    # Add brain-like circular structure
    brain_mask = (x - center_x)**2 + (y - center_y)**2 < (min(size) // 3)**2
    image_array[brain_mask] = np.random.randint(100, 180, np.sum(brain_mask))
    
    # Add some "lesion-like" spots
    for i in range(3):
        lesion_x = center_x + np.random.randint(-100, 100)
        lesion_y = center_y + np.random.randint(-100, 100)
        lesion_mask = (x - lesion_x)**2 + (y - lesion_y)**2 < 400
        image_array[lesion_mask] = np.random.randint(80, 120, np.sum(lesion_mask))
    
    # Convert to PIL Image
    image = Image.fromarray(image_array, mode='L')
    if format.upper() != 'L':
        image = image.convert('RGB')
    
    return image

def test_mri_processor():
    """Test the MRI processor functions"""
    print("🧪 Testing MRI Processor...")
    
    try:
        from api.mri_analysis import MRIProcessor
        
        # Create test image
        test_image = create_test_image()
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        test_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        file_content = img_bytes.getvalue()
        
        print(f"   ✅ Created test image: {len(file_content)} bytes")
        
        # Test validation
        validation_result = MRIProcessor.validate_mri_image(file_content, "test_brain_scan.png")
        print(f"   ✅ Validation result: {validation_result}")
        
        if validation_result["valid"]:
            print("   ✅ Image validation passed")
        else:
            print(f"   ❌ Image validation failed: {validation_result.get('error')}")
            return False
            
        return True
        
    except Exception as e:
        print(f"   ❌ MRI Processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_background_processing():
    """Test the background processing function"""
    print("🔄 Testing background processing...")
    
    try:
        from api.mri_analysis import process_mri_analysis_background
        
        # Create test image
        test_image = create_test_image()
        img_bytes = io.BytesIO()
        test_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        file_content = img_bytes.getvalue()
        
        test_file_path = os.path.join("uploads", "mri", "test_image.png")
        
        print(f"   📁 Test file path: {test_file_path}")
        print(f"   📊 File content size: {len(file_content)} bytes")
        
        # Note: We can't test the full background processing without database setup
        # But we can test the image processing parts
        
        # Test PIL operations
        image = Image.open(io.BytesIO(file_content))
        print(f"   🖼️  Image loaded: {image.size}, format: {image.format}, mode: {image.mode}")
        
        # Test conversion
        if image.mode not in ['L', 'LA']:
            image_gray = image.convert('L')
            print(f"   🎨 Converted to grayscale: {image_gray.mode}")
        
        # Test resize
        analysis_size = (512, 512)
        image_resized = image.resize(analysis_size, Image.Resampling.LANCZOS)
        print(f"   📏 Resized for analysis: {image_resized.size}")
        
        print("   ✅ Background processing components working")
        return True
        
    except Exception as e:
        print(f"   ❌ Background processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_directory_setup():
    """Test directory setup and permissions"""
    print("📁 Testing directory setup...")
    
    upload_dir = "uploads/mri"
    
    try:
        # Check if directory exists
        exists = os.path.exists(upload_dir)
        print(f"   📂 Directory exists: {exists}")
        
        if not exists:
            os.makedirs(upload_dir, exist_ok=True)
            print(f"   ✅ Created directory: {upload_dir}")
        
        # Check permissions
        readable = os.access(upload_dir, os.R_OK)
        writable = os.access(upload_dir, os.W_OK)
        
        print(f"   🔍 Directory readable: {readable}")
        print(f"   ✏️  Directory writable: {writable}")
        
        # Test file operations
        test_file = os.path.join(upload_dir, "test_permissions.txt")
        try:
            with open(test_file, "w") as f:
                f.write("test")
            
            with open(test_file, "r") as f:
                content = f.read()
            
            os.remove(test_file)
            print("   ✅ File operations working")
            return True
            
        except Exception as file_error:
            print(f"   ❌ File operations failed: {file_error}")
            return False
        
    except Exception as e:
        print(f"   ❌ Directory setup test failed: {e}")
        return False

def test_imports():
    """Test all required imports"""
    print("📦 Testing imports...")
    
    try:
        import numpy as np
        print(f"   ✅ NumPy: {np.__version__}")
        
        from PIL import Image
        print(f"   ✅ Pillow (PIL): {Image.__version__ if hasattr(Image, '__version__') else 'Available'}")
        
        import json
        print("   ✅ JSON: Available")
        
        from datetime import datetime
        print("   ✅ DateTime: Available")
        
        from sqlalchemy.sql import func
        print("   ✅ SQLAlchemy: Available")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔬 MRI Processing Diagnostic Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Directory Setup", test_directory_setup), 
        ("MRI Processor", test_mri_processor),
        ("Background Processing", test_background_processing)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"   ❌ Test crashed: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! MRI processing should work correctly.")
        print("\nIf you're still experiencing issues:")
        print("1. Check the backend logs for specific error messages")
        print("2. Verify the database tables exist (run database migrations)")
        print("3. Ensure authentication is working properly")
        print("4. Try using the /api/mri/test-upload endpoint for debugging")
    else:
        print("⚠️  SOME TESTS FAILED! Check the errors above.")
        print("This might explain why MRI processing is failing.")
    
    return all_passed

if __name__ == "__main__":
    main()
