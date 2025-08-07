#!/usr/bin/env python3
"""
Debug test to identify the exact error in brain tumor detection
"""

import sys
import logging
from PIL import Image, ImageDraw
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_simple_test_image():
    """Create a simple test brain image"""
    img = Image.new('L', (300, 300), color=50)
    draw = ImageDraw.Draw(img)
    
    # Simple brain outline
    draw.ellipse([50, 50, 250, 250], fill=100, outline=120)
    
    # Add a bright spot (tumor-like)
    draw.ellipse([140, 110, 160, 130], fill=180)
    
    img.save("debug_test.jpg")
    return "debug_test.jpg"

def test_analysis_function():
    """Test the analysis function directly"""
    logger.info("Testing analysis function directly...")
    
    try:
        # Import the analysis function
        sys.path.append('.')
        from api.mri_analysis import analyze_mri_image_real
        
        # Create test image
        test_image_path = create_simple_test_image()
        test_image = Image.open(test_image_path)
        
        logger.info(f"Test image created: {test_image_path}")
        logger.info(f"Image size: {test_image.size}, mode: {test_image.mode}")
        
        # Run analysis
        result = analyze_mri_image_real(test_image)
        
        logger.info("Analysis completed successfully!")
        logger.info(f"Result status: {result.get('status')}")
        
        if result.get('status') == 'success':
            overall = result.get('overall_assessment', {})
            logger.info(f"Risk level: {overall.get('risk_level')}")
            logger.info(f"Regions found: {overall.get('num_regions_detected')}")
        else:
            logger.error(f"Analysis failed: {result.get('message')}")
        
        return True
        
    except Exception as e:
        logger.error(f"Direct analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Cleanup
        import os
        if os.path.exists("debug_test.jpg"):
            os.remove("debug_test.jpg")

if __name__ == "__main__":
    logger.info("🐛 Debug Test - Direct Analysis Function")
    success = test_analysis_function()
    
    if success:
        logger.info("✅ Direct analysis function works!")
        logger.info("The issue might be in the API endpoint or request handling.")
    else:
        logger.error("❌ Direct analysis function has issues!")
        logger.error("The problem is in the core analysis algorithm.")
