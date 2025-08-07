#!/usr/bin/env python3
"""
Image Model Validation Script for CuraGenie
"""

import numpy as np
import tensorflow as tf
import sys

def validate_image_model(model_path):
    print("🧪 CuraGenie Image Model Validation")
    print("=" * 50)
    
    # Test 1: Model Loading
    print("\n📁 Test 1: Model Loading")
    try:
        model = tf.keras.models.load_model(model_path)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False
    
    # Test 2: Input/Output Shape
    print("\n📊 Test 2: Input/Output Shape")
    try:
        input_shape = model.input_shape
        output_shape = model.output_shape
        
        # Expected shape: (None, height, width, channels)
        if len(input_shape) != 4 or input_shape[1:] != (150, 150, 3):
            print(f"❌ Unexpected input shape: {input_shape}")
            return False
        print(f"✅ Correct input shape: {input_shape}")
        
        # Expected shape: (None, num_classes)
        if len(output_shape) != 2 or output_shape[1] != 4:
            print(f"❌ Unexpected output shape: {output_shape}")
            return False
        print(f"✅ Correct output shape: {output_shape}")
        
    except Exception as e:
        print(f"❌ Shape validation failed: {e}")
        return False

    print("\n🎉 ALL TESTS PASSED!")
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_image_model.py <path_to_model.h5>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    
    if validate_image_model(model_path):
        print("\n🚀 Ready for deployment!")
        sys.exit(0)
    else:
        print("\n⚠️ Model validation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()

