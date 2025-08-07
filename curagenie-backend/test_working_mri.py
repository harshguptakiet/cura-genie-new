#!/usr/bin/env python3
"""
Test the working MRI analysis API
"""

import os
import requests
import logging
from PIL import Image, ImageDraw
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

def create_test_mri_image(has_tumor=True, filename="test_mri.jpg"):
    """Create a test MRI-like image"""
    img = Image.new('RGB', (300, 300), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Draw brain outline
    draw.ellipse([50, 50, 250, 250], fill=(80, 80, 80), outline=(120, 120, 120))
    draw.ellipse([70, 70, 230, 230], fill=(100, 100, 100), outline=(140, 140, 140))
    
    # Add some brain texture
    np.random.seed(42 if has_tumor else 123)
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
    
    img.save(filename)
    logger.info(f"Saved test image: {filename}")
    return filename

def test_mri_analysis():
    """Test the working MRI analysis"""
    logger.info("🧠 Testing Working MRI Analysis System")
    
    # Test system status
    response = requests.get(f"{BASE_URL}/api/mri/test")
    if response.status_code == 200:
        logger.info("✅ MRI API is working")
    else:
        logger.error(f"❌ MRI API test failed: {response.status_code}")
        return False
    
    # Create test image
    test_image = create_test_mri_image(has_tumor=True)
    
    # Test real analysis without auth
    try:
        with open(test_image, 'rb') as f:
            files = {'file': (test_image, f, 'image/jpeg')}
            response = requests.post(f"{BASE_URL}/api/mri/test-real-analysis", files=files)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                logger.info("✅ MRI Real Analysis Test successful:")
                
                # Display analysis results
                analysis_result = data.get('analysis_result', {})
                if analysis_result.get('status') == 'success':
                    overall = analysis_result.get('overall_assessment', {})
                    logger.info(f"   - Risk Level: {overall.get('risk_level')}")
                    logger.info(f"   - Confidence: {overall.get('confidence')}")
                    logger.info(f"   - Regions Found: {overall.get('num_regions_detected')}")
                    logger.info(f"   - Total Volume: {overall.get('total_tumor_volume_mm3')} mm³")
                    
                    regions = analysis_result.get('detected_regions', [])
                    if regions:
                        logger.info(f"   - Detected regions:")
                        for i, region in enumerate(regions):
                            logger.info(f"     • {region.get('type')} (confidence: {region.get('confidence')})")
                    
                    return True
                else:
                    logger.error(f"❌ Analysis failed: {analysis_result.get('message')}")
            else:
                logger.error(f"❌ Test failed: {data.get('error')}")
        else:
            logger.error(f"❌ Request failed: {response.status_code}")
            
    except Exception as e:
        logger.error(f"❌ Test error: {e}")
    finally:
        if os.path.exists(test_image):
            os.remove(test_image)
    
    return False

if __name__ == "__main__":
    success = test_mri_analysis()
    if success:
        logger.info("🎉 Working MRI Analysis System test passed!")
    else:
        logger.error("❌ Test failed")
