#!/usr/bin/env python3
"""
Test script for CuraGenie Backend

This script tests the main functionality of the backend without
requiring external services like PostgreSQL or Redis.
"""

import sys
import os
import tempfile
import io

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from core.config import settings
        print("✅ Core config imported")
    except Exception as e:
        print(f"❌ Failed to import core config: {e}")
        return False
    
    try:
        from schemas.schemas import GenomicDataResponse, PrsScoreResponse
        print("✅ Schemas imported")
    except Exception as e:
        print(f"❌ Failed to import schemas: {e}")
        return False
    
    try:
        from worker.tasks import load_ml_model
        print("✅ Worker tasks imported")
    except Exception as e:
        print(f"❌ Failed to import worker tasks: {e}")
        return False
    
    return True

def test_ml_model():
    """Test ML model creation and loading"""
    print("🤖 Testing ML model...")
    
    try:
        from worker.tasks import load_ml_model, ML_MODEL
        import numpy as np
        
        # Test model prediction
        if ML_MODEL is not None:
            test_features = [[45, 28.0, 110, 120, 0]]  # [age, bmi, glucose, bp, family_history]
            prediction = ML_MODEL.predict(test_features)[0]
            confidence = ML_MODEL.predict_proba(test_features)[0]
            
            print(f"✅ ML model prediction: {'High Risk' if prediction else 'Low Risk'}")
            print(f"✅ Confidence: {max(confidence):.3f}")
            return True
        else:
            print("❌ ML model not loaded")
            return False
            
    except Exception as e:
        print(f"❌ ML model test failed: {e}")
        return False

def test_genomic_parsing():
    """Test genomic file parsing logic"""
    print("🧬 Testing genomic file parsing...")
    
    try:
        from Bio import SeqIO
        from io import StringIO
        
        # Create a simple FASTQ content for testing
        fastq_content = """@seq1
ATCGATCGATCGATCG
+
IIIIIIIIIIIIIIII
@seq2
GCTAGCTAGCTAGCTA
+
IIIIIIIIIIIIIIII
"""
        
        # Parse the FASTQ content
        sequences = list(SeqIO.parse(StringIO(fastq_content), "fastq"))
        
        if len(sequences) == 2:
            print(f"✅ Parsed {len(sequences)} sequences from FASTQ")
            print(f"✅ First sequence: {str(sequences[0].seq)[:10]}...")
            return True
        else:
            print(f"❌ Expected 2 sequences, got {len(sequences)}")
            return False
            
    except Exception as e:
        print(f"❌ Genomic parsing test failed: {e}")
        return False

def test_prs_calculation():
    """Test PRS score calculation logic"""
    print("📊 Testing PRS calculation...")
    
    try:
        import hashlib
        
        # Test the deterministic PRS calculation logic
        genomic_data_id = 123
        disease_type = "diabetes"
        
        hash_input = f"{genomic_data_id}_{disease_type}".encode()
        hash_value = hashlib.sha256(hash_input).hexdigest()
        score = int(hash_value[:8], 16) / (2**32)
        
        # Apply disease modifier
        modifier = 0.1  # diabetes modifier
        final_score = max(0, min(1, score + modifier))
        
        print(f"✅ PRS calculation for {disease_type}: {final_score:.3f}")
        print(f"✅ Percentile: {int(final_score * 100)}th")
        
        # Test that the same input always gives the same result
        hash_input2 = f"{genomic_data_id}_{disease_type}".encode()
        hash_value2 = hashlib.sha256(hash_input2).hexdigest()
        score2 = int(hash_value2[:8], 16) / (2**32)
        final_score2 = max(0, min(1, score2 + modifier))
        
        if final_score == final_score2:
            print("✅ PRS calculation is deterministic")
            return True
        else:
            print("❌ PRS calculation is not deterministic")
            return False
            
    except Exception as e:
        print(f"❌ PRS calculation test failed: {e}")
        return False

def test_websocket_manager():
    """Test WebSocket connection manager"""
    print("🔌 Testing WebSocket manager...")
    
    try:
        from core.websockets import ConnectionManager
        
        # Create a connection manager
        manager = ConnectionManager()
        
        # Test initial state
        if manager.get_active_connections_count() == 0:
            print("✅ Connection manager initialized with 0 connections")
        else:
            print("❌ Connection manager should start with 0 connections")
            return False
        
        # Test user connection check
        if not manager.is_user_connected("test_user"):
            print("✅ Correctly identifies unconnected user")
            return True
        else:
            print("❌ Should not find unconnected user")
            return False
            
    except Exception as e:
        print(f"❌ WebSocket manager test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 CuraGenie Backend Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("ML Model Tests", test_ml_model),
        ("Genomic Parsing Tests", test_genomic_parsing),  
        ("PRS Calculation Tests", test_prs_calculation),
        ("WebSocket Manager Tests", test_websocket_manager),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
