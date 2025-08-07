#!/usr/bin/env python3
"""
Test script for Enhanced MRI Analysis System
"""

import os
import sys
import requests
import json
import time
import logging
from PIL import Image, ImageDraw
import numpy as np
import io

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:8000"
ENHANCED_MRI_URL = f"{BASE_URL}/api/enhanced-mri"

def create_test_mri_image(has_tumor=True, filename="test_mri.jpg"):
    """
    Create a test MRI-like image for testing
    """
    logger.info(f"Creating test MRI image: {filename} (has_tumor={has_tumor})")
    
    # Create base brain-like image
    img = Image.new('RGB', (300, 300), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Draw brain outline
    draw.ellipse([50, 50, 250, 250], fill=(80, 80, 80), outline=(120, 120, 120))
    draw.ellipse([70, 70, 230, 230], fill=(100, 100, 100), outline=(140, 140, 140))
    
    # Add some brain texture
    for _ in range(50):
        x = np.random.randint(70, 230)
        y = np.random.randint(70, 230)
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(120, 120, 120))
    
    if has_tumor:
        # Add tumor-like bright spot
        tumor_x, tumor_y = 150, 120
        draw.ellipse([tumor_x-15, tumor_y-15, tumor_x+15, tumor_y+15], fill=(200, 200, 200))
        draw.ellipse([tumor_x-10, tumor_y-10, tumor_x+10, tumor_y+10], fill=(220, 220, 220))
        logger.info(f"Added tumor at position ({tumor_x}, {tumor_y})")
    
    # Save image
    img.save(filename)
    logger.info(f"Saved test image: {filename}")
    return filename

def test_model_info():
    """
    Test the model info endpoint
    """
    logger.info("🔍 Testing model info endpoint...")
    
    try:
        response = requests.get(f"{ENHANCED_MRI_URL}/model-info")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ Model info retrieved successfully:")
            logger.info(f"   - Model loaded: {data['model_loaded']}")
            logger.info(f"   - Model exists: {data['model_file_exists']}")
            logger.info(f"   - Total params: {data['model_architecture']['total_params']}")
            return True
        else:
            logger.error(f"❌ Model info request failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Model info test failed: {e}")
        return False

def test_system_status():
    """
    Test the system status endpoint
    """
    logger.info("🔍 Testing system status endpoint...")
    
    try:
        response = requests.get(f"{ENHANCED_MRI_URL}/test")
        
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ System status retrieved successfully:")
            logger.info(f"   - Message: {data['message']}")
            logger.info(f"   - CNN Model loaded: {data['model_status']['cnn_model_loaded']}")
            logger.info(f"   - Upload dir exists: {data['directory_exists']}")
            return True
        else:
            logger.error(f"❌ System status request failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ System status test failed: {e}")
        return False

def test_cnn_analysis_no_auth(image_path):
    """
    Test CNN analysis without authentication
    """
    logger.info(f"🧠 Testing CNN analysis without auth using: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, 'image/jpeg')}
            response = requests.post(f"{ENHANCED_MRI_URL}/test-cnn-analysis", files=files)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                logger.info("✅ CNN analysis test successful:")
                
                # Display file info
                file_info = data.get('file_info', {})
                logger.info(f"   - Filename: {file_info.get('filename')}")
                logger.info(f"   - Image size: {file_info.get('image_size')}")
                logger.info(f"   - File size: {file_info.get('size')} bytes")
                
                # Display model info
                model_info = data.get('model_info', {})
                logger.info(f"   - Model loaded: {model_info.get('model_loaded')}")
                logger.info(f"   - Model exists: {model_info.get('model_exists')}")
                
                # Display analysis results
                analysis_result = data.get('analysis_result', {})
                if analysis_result.get('status') == 'success':
                    overall = analysis_result.get('overall_assessment', {})
                    logger.info("   - Analysis Results:")
                    logger.info(f"     • Tumor detected: {overall.get('tumor_detected')}")
                    logger.info(f"     • Tumor probability: {overall.get('tumor_probability')}")
                    logger.info(f"     • Risk level: {overall.get('risk_level')}")
                    logger.info(f"     • Confidence: {overall.get('confidence')}")
                    
                    regions = analysis_result.get('detected_regions', [])
                    if regions:
                        logger.info(f"     • Detected regions: {len(regions)}")
                        for i, region in enumerate(regions):
                            logger.info(f"       - Region {i+1}: {region.get('type')} (confidence: {region.get('confidence')})")
                else:
                    logger.warning(f"⚠️ Analysis failed: {analysis_result.get('message')}")
                
                return True
            else:
                logger.error(f"❌ CNN analysis failed: {data.get('error')}")
                return False
        else:
            logger.error(f"❌ CNN analysis request failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ CNN analysis test failed: {e}")
        return False

def test_full_workflow_with_auth():
    """
    Test full workflow with authentication (requires valid token)
    Note: This will only work if you have valid authentication
    """
    logger.info("🔐 Testing full workflow with authentication...")
    logger.info("⚠️ Note: This requires valid authentication token")
    
    # This would need a real auth token
    headers = {
        'Authorization': 'Bearer YOUR_TOKEN_HERE'
    }
    
    # Create test image
    test_image = create_test_mri_image(has_tumor=True, filename="test_mri_with_auth.jpg")
    
    try:
        # Upload image
        with open(test_image, 'rb') as f:
            files = {'file': (test_image, f, 'image/jpeg')}
            response = requests.post(f"{ENHANCED_MRI_URL}/upload", files=files, headers=headers)
        
        if response.status_code == 202:  # Accepted
            data = response.json()
            analysis_id = data['id']
            logger.info(f"✅ Upload successful, analysis ID: {analysis_id}")
            
            # Poll for results
            max_attempts = 30
            for attempt in range(max_attempts):
                time.sleep(2)
                
                result_response = requests.get(f"{ENHANCED_MRI_URL}/analysis/{analysis_id}", headers=headers)
                
                if result_response.status_code == 200:
                    result_data = result_response.json()
                    status = result_data.get('status')
                    
                    logger.info(f"   Attempt {attempt + 1}: Status = {status}")
                    
                    if status == 'completed':
                        logger.info("✅ Analysis completed successfully!")
                        results = json.loads(result_data.get('results_json', '{}'))
                        overall = results.get('overall_assessment', {})
                        logger.info(f"   - Tumor detected: {overall.get('tumor_detected')}")
                        logger.info(f"   - Risk level: {overall.get('risk_level')}")
                        logger.info(f"   - Confidence: {overall.get('confidence')}")
                        return True
                    elif status == 'failed':
                        logger.error(f"❌ Analysis failed: {result_data.get('error_message')}")
                        return False
                else:
                    logger.error(f"❌ Failed to get analysis results: {result_response.status_code}")
                    return False
            
            logger.warning("⚠️ Analysis didn't complete within timeout")
            return False
            
        elif response.status_code == 401:
            logger.warning("⚠️ Authentication required - skipping full workflow test")
            logger.info("   To test with auth, provide a valid bearer token")
            return None  # Skip this test
        else:
            logger.error(f"❌ Upload failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Full workflow test failed: {e}")
        return False
    finally:
        # Clean up test image
        if os.path.exists(test_image):
            os.remove(test_image)

def main():
    """
    Run all tests for the enhanced MRI analysis system
    """
    logger.info("🚀 Starting Enhanced MRI Analysis System Tests")
    logger.info("="*50)
    
    # Test 1: System status
    logger.info("\n📋 Test 1: System Status")
    status_ok = test_system_status()
    
    # Test 2: Model info
    logger.info("\n📋 Test 2: Model Information")
    model_ok = test_model_info()
    
    # Test 3: Create test images
    logger.info("\n📋 Test 3: Creating Test Images")
    tumor_image = create_test_mri_image(has_tumor=True, filename="test_tumor_mri.jpg")
    normal_image = create_test_mri_image(has_tumor=False, filename="test_normal_mri.jpg")
    
    # Test 4: CNN analysis (no auth) - tumor image
    logger.info("\n📋 Test 4: CNN Analysis - Tumor Image (No Auth)")
    tumor_analysis_ok = test_cnn_analysis_no_auth(tumor_image)
    
    # Test 5: CNN analysis (no auth) - normal image
    logger.info("\n📋 Test 5: CNN Analysis - Normal Image (No Auth)")
    normal_analysis_ok = test_cnn_analysis_no_auth(normal_image)
    
    # Test 6: Full workflow with auth (optional)
    logger.info("\n📋 Test 6: Full Workflow with Authentication")
    auth_workflow_ok = test_full_workflow_with_auth()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*50)
    
    tests = [
        ("System Status", status_ok),
        ("Model Information", model_ok),
        ("CNN Analysis - Tumor", tumor_analysis_ok),
        ("CNN Analysis - Normal", normal_analysis_ok),
        ("Full Workflow with Auth", auth_workflow_ok)
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test_name, result in tests:
        if result is True:
            logger.info(f"✅ {test_name}: PASSED")
            passed += 1
        elif result is False:
            logger.info(f"❌ {test_name}: FAILED")
            failed += 1
        else:
            logger.info(f"⏭️ {test_name}: SKIPPED")
            skipped += 1
    
    logger.info(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        logger.info("🎉 All available tests passed!")
    else:
        logger.warning(f"⚠️ {failed} test(s) failed")
    
    # Cleanup test images
    for img in [tumor_image, normal_image]:
        if os.path.exists(img):
            os.remove(img)
            logger.info(f"🧹 Cleaned up: {img}")
    
    return failed == 0

if __name__ == "__main__":
    """
    Run the test suite
    
    Usage:
    python test_enhanced_mri.py
    
    Make sure the CuraGenie backend is running at http://localhost:8000
    """
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            logger.error("❌ CuraGenie backend is not responding properly")
            logger.error("   Please start the backend server with: python main.py")
            sys.exit(1)
    except requests.exceptions.RequestException:
        logger.error("❌ Cannot connect to CuraGenie backend")
        logger.error("   Please start the backend server with: python main.py")
        sys.exit(1)
    
    logger.info("✅ CuraGenie backend is running")
    
    # Run tests
    success = main()
    sys.exit(0 if success else 1)
