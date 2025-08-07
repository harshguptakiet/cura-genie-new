#!/usr/bin/env python3
"""
Model Validation Script for CuraGenie

Use this script to test if your pre-trained model meets the requirements
before providing it to replace the dummy model.
"""

import pickle
import numpy as np
import sys

def validate_model(model_path):
    """
    Validates if a model meets CuraGenie's interface requirements
    
    Args:
        model_path (str): Path to the pickle model file
    
    Returns:
        bool: True if model passes all tests
    """
    print("🧪 CuraGenie Model Validation")
    print("=" * 50)
    
    # Test 1: Model Loading
    print("\n📁 Test 1: Model Loading")
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False
    
    # Test 2: Required Methods
    print("\n🔧 Test 2: Required Methods")
    
    # Check predict method
    if not hasattr(model, 'predict'):
        print("❌ Model missing 'predict' method")
        return False
    print("✅ predict() method found")
    
    # Check predict_proba method
    if not hasattr(model, 'predict_proba'):
        print("❌ Model missing 'predict_proba' method")
        return False
    print("✅ predict_proba() method found")
    
    # Test 3: Input Format
    print("\n📊 Test 3: Input Format")
    
    test_cases = [
        [2, 120, 70, 20, 80, 25.0, 0.4, 30],   # Low risk
        [6, 148, 72, 35, 0, 33.6, 0.627, 50], # High risk
        [1, 89, 66, 23, 94, 28.1, 0.167, 21],  # Low risk
    ]
    
    for i, features in enumerate(test_cases):
        try:
            # Test predict method
            prediction = model.predict([features])
            if len(prediction) != 1:
                print(f"❌ predict() should return array of length 1, got {len(prediction)}")
                return False
            
            pred_value = prediction[0]
            if pred_value not in [0, 1]:
                print(f"❌ predict() should return 0 or 1, got {pred_value}")
                return False
            
            # Test predict_proba method
            probabilities = model.predict_proba([features])
            if len(probabilities) != 1:
                print(f"❌ predict_proba() should return array of length 1, got {len(probabilities)}")
                return False
            
            proba_values = probabilities[0]
            if len(proba_values) != 2:
                print(f"❌ predict_proba() should return 2 probabilities, got {len(proba_values)}")
                return False
            
            # Check probabilities sum to 1
            prob_sum = sum(proba_values)
            if abs(prob_sum - 1.0) > 0.001:
                print(f"❌ Probabilities should sum to 1.0, got {prob_sum}")
                return False
            
            print(f"✅ Test case {i+1}: prediction={pred_value}, probabilities={proba_values}")
            
        except Exception as e:
            print(f"❌ Error with test case {i+1}: {e}")
            return False
    
    # Test 4: Output Consistency
    print("\n🔄 Test 4: Output Consistency")
    
    # Same input should give same output
    test_input = [6, 148, 72, 35, 0, 33.6, 0.627, 50]
    
    try:
        pred1 = model.predict([test_input])[0]
        pred2 = model.predict([test_input])[0]
        
        proba1 = model.predict_proba([test_input])[0]
        proba2 = model.predict_proba([test_input])[0]
        
        if pred1 != pred2:
            print(f"❌ Inconsistent predictions: {pred1} vs {pred2}")
            return False
        
        if not np.allclose(proba1, proba2):
            print(f"❌ Inconsistent probabilities: {proba1} vs {proba2}")
            return False
        
        print("✅ Model outputs are consistent")
        
    except Exception as e:
        print(f"❌ Consistency test failed: {e}")
        return False
    
    # Test 5: Edge Cases
    print("\n🚨 Test 5: Edge Cases")
    
    edge_cases = [
        [0, 50, 40, 10, 0, 18.0, 0.1, 21],      # Minimum values
        [17, 200, 120, 100, 850, 60.0, 2.4, 85],# Maximum values
        [3, 120, 80, 30, 150, 32.0, 0.5, 45],   # Average values
    ]
    
    for i, features in enumerate(edge_cases):
        try:
            prediction = model.predict([features])[0]
            probabilities = model.predict_proba([features])[0]
            
            # Check for valid outputs
            if prediction not in [0, 1]:
                print(f"❌ Edge case {i+1}: Invalid prediction {prediction}")
                return False
            
            if any(p < 0 or p > 1 for p in probabilities):
                print(f"❌ Edge case {i+1}: Invalid probabilities {probabilities}")
                return False
            
            print(f"✅ Edge case {i+1}: OK")
            
        except Exception as e:
            print(f"❌ Edge case {i+1} failed: {e}")
            return False
    
    # Test 6: Performance Summary
    print("\n📈 Test 6: Performance Summary")
    
    # Test with multiple predictions
    test_features = [
        [1, 85, 66, 29, 0, 26.6, 0.351, 31],
        [8, 183, 64, 0, 0, 23.3, 0.672, 32],
        [1, 89, 66, 23, 94, 28.1, 0.167, 21],
        [0, 137, 40, 35, 168, 43.1, 2.288, 33],
        [5, 116, 74, 0, 0, 25.6, 0.201, 30],
    ]
    
    predictions = []
    probabilities = []
    
    for features in test_features:
        pred = model.predict([features])[0]
        prob = model.predict_proba([features])[0]
        predictions.append(pred)
        probabilities.append(prob)
    
    high_risk_count = sum(predictions)
    avg_confidence = np.mean([max(prob) for prob in probabilities])
    
    print(f"✅ Sample predictions: {predictions}")
    print(f"✅ High risk cases: {high_risk_count}/{len(predictions)}")
    print(f"✅ Average confidence: {avg_confidence:.3f}")
    
    # Final validation
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("✅ Your model is compatible with CuraGenie!")
    print("✅ You can safely provide this model for replacement.")
    
    return True

def main():
    """Main function to run validation"""
    if len(sys.argv) != 2:
        print("Usage: python validate_model.py <path_to_model.pkl>")
        print("Example: python validate_model.py my_diabetes_model.pkl")
        sys.exit(1)
    
    model_path = sys.argv[1]
    
    try:
        if validate_model(model_path):
            print("\n🚀 Ready for deployment!")
            sys.exit(0)
        else:
            print("\n⚠️  Model validation failed. Please fix the issues above.")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Validation error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
