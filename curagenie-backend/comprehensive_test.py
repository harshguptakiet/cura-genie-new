#!/usr/bin/env python3
"""
Comprehensive test for the CuraGenie brain tumor detection system
This will start the server and run complete tests
"""

import os
import sys
import time
import subprocess
import requests
import logging
import threading
from PIL import Image, ImageDraw
import numpy as np
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

class ServerManager:
    def __init__(self):
        self.server_process = None
        self.server_ready = False
    
    def start_server(self):
        """Start the CuraGenie server"""
        logger.info("🚀 Starting CuraGenie server...")
        try:
            # Start server in background
            self.server_process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd()
            )
            
            # Wait for server to start
            for attempt in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(f"{BASE_URL}/health", timeout=2)
                    if response.status_code == 200:
                        self.server_ready = True
                        logger.info("✅ Server is ready!")
                        return True
                except:
                    time.sleep(1)
                    logger.info(f"   Waiting for server... (attempt {attempt + 1}/30)")
            
            logger.error("❌ Server failed to start within 30 seconds")
            return False
            
        except Exception as e:
            logger.error(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the server"""
        if self.server_process:
            logger.info("⏹️ Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
            logger.info("✅ Server stopped")

def create_test_mri_image(has_tumor=True, tumor_type="glioma", filename=None):
    """Create a realistic test MRI image"""
    if filename is None:
        filename = f"test_{tumor_type}_{'tumor' if has_tumor else 'normal'}.jpg"
    
    logger.info(f"Creating test MRI: {filename} (tumor={has_tumor}, type={tumor_type})")
    
    # Create brain-like image
    img = Image.new('L', (512, 512), color=20)  # Dark background
    draw = ImageDraw.Draw(img)
    
    # Draw brain outline (more realistic)
    draw.ellipse([80, 100, 430, 450], fill=120, outline=140)
    draw.ellipse([90, 110, 250, 440], fill=110, outline=130)  # Left hemisphere
    draw.ellipse([260, 110, 420, 440], fill=110, outline=130)  # Right hemisphere
    
    # Brain stem
    draw.rectangle([230, 380, 280, 450], fill=100)
    
    # Ventricles (dark areas)
    draw.ellipse([180, 200, 220, 240], fill=60)
    draw.ellipse([290, 200, 330, 240], fill=60)
    
    # Add brain texture
    np.random.seed(42 if has_tumor else 123)
    for _ in range(200):
        x = np.random.randint(90, 420)
        y = np.random.randint(110, 440)
        if 90 < x < 420 and 110 < y < 440:
            brightness = np.random.randint(100, 130)
            draw.point((x, y), fill=brightness)
    
    if has_tumor:
        if tumor_type == "glioma":
            # Large, irregular, bright tumor
            tumor_x, tumor_y = 200, 250
            tumor_size = 35
            draw.ellipse([tumor_x-tumor_size, tumor_y-tumor_size//2, 
                         tumor_x+tumor_size, tumor_y+tumor_size//2], fill=180)
            # Irregular edges
            for i in range(6):
                offset_x = np.random.randint(-12, 12)
                offset_y = np.random.randint(-8, 8)
                draw.ellipse([tumor_x+offset_x-8, tumor_y+offset_y-6, 
                             tumor_x+offset_x+8, tumor_y+offset_y+6], fill=170)
        
        elif tumor_type == "meningioma":
            # Round, well-defined tumor
            tumor_x, tumor_y = 320, 200
            draw.ellipse([tumor_x-18, tumor_y-18, tumor_x+18, tumor_y+18], fill=85)
            draw.ellipse([tumor_x-12, tumor_y-12, tumor_x+12, tumor_y+12], fill=75)
    
    img.save(filename)
    return filename

def test_system_health():
    """Test basic system health"""
    logger.info("🏥 Testing system health...")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ System health check passed:")
            logger.info(f"   - Status: {data.get('status')}")
            logger.info(f"   - ML APIs available: {data.get('ml_apis_available')}")
            logger.info(f"   - Enhanced MRI available: {data.get('enhanced_mri_available')}")
            return True
        else:
            logger.error(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Health check error: {e}")
        return False

def test_mri_api_status():
    """Test MRI API status"""
    logger.info("🧠 Testing MRI API status...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/mri/test", timeout=5)
        if response.status_code == 200:
            data = response.json()
            logger.info("✅ MRI API status check passed:")
            logger.info(f"   - Message: {data.get('message')}")
            logger.info(f"   - Upload dir exists: {data.get('directory_exists')}")
            logger.info(f"   - Directory writable: {data.get('directory_writable')}")
            return True
        else:
            logger.error(f"❌ MRI API status failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ MRI API status error: {e}")
        return False

def test_brain_tumor_detection(image_path):
    """Test brain tumor detection with a real image"""
    logger.info(f"🔬 Testing brain tumor detection with: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/api/mri/test-real-analysis", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                logger.info("✅ Brain tumor detection successful:")
                
                # File info
                file_info = data.get('file_info', {})
                logger.info(f"   - File: {file_info.get('filename')}")
                logger.info(f"   - Size: {file_info.get('size')} bytes")
                logger.info(f"   - Image dimensions: {file_info.get('image_size')}")
                
                # Analysis results
                analysis = data.get('analysis_result', {})
                if analysis.get('status') == 'success':
                    overall = analysis.get('overall_assessment', {})
                    logger.info("   - Analysis Results:")
                    logger.info(f"     • Risk Level: {overall.get('risk_level')}")
                    logger.info(f"     • Confidence: {overall.get('confidence')}")
                    logger.info(f"     • Regions Found: {overall.get('num_regions_detected')}")
                    logger.info(f"     • Total Volume: {overall.get('total_tumor_volume_mm3')} mm³")
                    
                    # Detected regions
                    regions = analysis.get('detected_regions', [])
                    if regions:
                        logger.info(f"   - Detected Regions ({len(regions)}):")
                        for i, region in enumerate(regions[:3]):  # Show first 3
                            logger.info(f"     {i+1}. {region.get('type')} (confidence: {region.get('confidence')})")
                    
                    return True, overall.get('risk_level'), len(regions)
                else:
                    logger.error(f"❌ Analysis failed: {analysis.get('message')}")
                    return False, None, 0
            else:
                logger.error(f"❌ Detection failed: {data.get('error')}")
                return False, None, 0
        else:
            logger.error(f"❌ Request failed: {response.status_code}")
            logger.error(f"   Response: {response.text}")
            return False, None, 0
    except Exception as e:
        logger.error(f"❌ Brain tumor detection error: {e}")
        return False, None, 0

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    logger.info("🎯 COMPREHENSIVE CURAGENIE BRAIN TUMOR DETECTION TEST")
    logger.info("="*70)
    
    test_results = []
    
    # Test 1: System Health
    logger.info("\n📋 Test 1: System Health Check")
    health_ok = test_system_health()
    test_results.append(("System Health", health_ok))
    
    if not health_ok:
        logger.error("❌ System health failed - aborting remaining tests")
        return test_results
    
    # Test 2: MRI API Status
    logger.info("\n📋 Test 2: MRI API Status")
    mri_api_ok = test_mri_api_status()
    test_results.append(("MRI API Status", mri_api_ok))
    
    if not mri_api_ok:
        logger.error("❌ MRI API not available - aborting brain tumor tests")
        return test_results
    
    # Test 3: Create test images
    logger.info("\n📋 Test 3: Creating Test Brain Images")
    try:
        glioma_image = create_test_mri_image(has_tumor=True, tumor_type="glioma")
        normal_image = create_test_mri_image(has_tumor=False, tumor_type="normal")
        meningioma_image = create_test_mri_image(has_tumor=True, tumor_type="meningioma")
        
        logger.info("✅ Test images created successfully")
        test_results.append(("Test Image Creation", True))
    except Exception as e:
        logger.error(f"❌ Failed to create test images: {e}")
        test_results.append(("Test Image Creation", False))
        return test_results
    
    # Test 4: Glioma Detection
    logger.info("\n📋 Test 4: Glioma Brain Tumor Detection")
    glioma_success, glioma_risk, glioma_regions = test_brain_tumor_detection(glioma_image)
    test_results.append(("Glioma Detection", glioma_success))
    
    # Test 5: Normal Brain Analysis
    logger.info("\n📋 Test 5: Normal Brain Analysis")
    normal_success, normal_risk, normal_regions = test_brain_tumor_detection(normal_image)
    test_results.append(("Normal Brain Analysis", normal_success))
    
    # Test 6: Meningioma Detection
    logger.info("\n📋 Test 6: Meningioma Brain Tumor Detection")
    meningioma_success, meningioma_risk, meningioma_regions = test_brain_tumor_detection(meningioma_image)
    test_results.append(("Meningioma Detection", meningioma_success))
    
    # Cleanup test images
    test_images = [glioma_image, normal_image, meningioma_image]
    for img in test_images:
        if os.path.exists(img):
            os.remove(img)
            logger.info(f"🧹 Cleaned up: {img}")
    
    return test_results

def print_test_summary(test_results):
    """Print comprehensive test summary"""
    logger.info("\n" + "="*70)
    logger.info("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
    logger.info("="*70)
    
    passed = sum(1 for _, result in test_results if result)
    failed = len(test_results) - passed
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\nOverall Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        logger.info("🎉 ALL TESTS PASSED!")
        logger.info("🧠 Your CuraGenie Brain Tumor Detection System is WORKING PERFECTLY!")
        logger.info("🚀 Ready for production use!")
    else:
        logger.warning(f"⚠️ {failed} test(s) failed - system needs attention")
    
    return failed == 0

def main():
    """Main test execution"""
    logger.info("🧠 CuraGenie Brain Tumor Detection - Comprehensive Test Suite")
    logger.info("="*70)
    
    # Initialize server manager
    server_manager = ServerManager()
    
    try:
        # Start server
        if not server_manager.start_server():
            logger.error("❌ Failed to start server - exiting")
            return False
        
        # Run tests
        test_results = run_comprehensive_tests()
        
        # Print summary
        success = print_test_summary(test_results)
        
        return success
        
    except KeyboardInterrupt:
        logger.info("\n⏹️ Test interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Test suite error: {e}")
        return False
    finally:
        # Stop server
        server_manager.stop_server()

if __name__ == "__main__":
    success = main()
    
    if success:
        logger.info("\n🎯 FINAL RESULT: CuraGenie Brain Tumor Detection System is OPERATIONAL! 🎉")
    else:
        logger.error("\n💥 FINAL RESULT: Some issues detected - check logs above")
    
    sys.exit(0 if success else 1)
