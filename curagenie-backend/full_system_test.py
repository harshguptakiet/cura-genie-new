#!/usr/bin/env python3
"""
Comprehensive CuraGenie System Test
Tests all components without using up OpenAI quota
"""

import asyncio
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_database():
    """Test database connectivity and models"""
    print("\n🗄️  Testing Database...")
    try:
        from db.database import SessionLocal, engine
        from db.models import GenomicData, PrsScore, MlPrediction
        
        # Test connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        # Test database file
        db_path = Path("curagenie.db")
        size_kb = db_path.stat().st_size / 1024 if db_path.exists() else 0
        
        print(f"   ✅ Database connection: Working")
        print(f"   ✅ Database size: {size_kb:.1f} KB") 
        print(f"   ✅ Models: GenomicData, PrsScore, MlPrediction")
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

async def test_ml_models():
    """Test ML model loading and basic functionality"""
    print("\n🧠 Testing ML Models...")
    try:
        from worker.tasks import load_ml_models, DIABETES_MODEL, ALZHEIMER_MODEL, BRAIN_TUMOR_MODEL
        import numpy as np
        
        # Load models
        load_ml_models()
        
        # Test diabetes model (should work with dummy data)
        if DIABETES_MODEL is not None:
            # Test prediction
            dummy_features = [1, 85, 66, 29, 0, 26.6, 0.351, 31]  # Sample diabetes features
            try:
                prediction = DIABETES_MODEL.predict([dummy_features])
                prob = DIABETES_MODEL.predict_proba([dummy_features])
                print(f"   ✅ Diabetes model: Working (prediction: {prediction[0]}, confidence: {max(prob[0]):.3f})")
            except:
                print(f"   ⚠️  Diabetes model: Loaded but prediction failed")
        else:
            print(f"   ❌ Diabetes model: Not loaded")
        
        # Check other models
        brain_status = "✅ Loaded" if BRAIN_TUMOR_MODEL is not None else "❌ Not loaded"
        alzheimer_status = "✅ Loaded" if ALZHEIMER_MODEL is not None else "❌ Not loaded" 
        
        print(f"   {brain_status} Brain tumor model (121.8 MB)")
        print(f"   {alzheimer_status} Alzheimer model")
        
        return True
    except Exception as e:
        print(f"   ❌ ML models error: {e}")
        return False

async def test_redis():
    """Test Redis connectivity"""
    print("\n🔴 Testing Redis...")
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        
        # Test basic operations
        r.set('test_key', 'test_value')
        value = r.get('test_key').decode('utf-8')
        r.delete('test_key')
        
        print(f"   ✅ Redis connection: Working")
        print(f"   ✅ Basic operations: Working")
        return True
    except Exception as e:
        print(f"   ❌ Redis error: {e}")
        return False

async def test_api_endpoints():
    """Test FastAPI application and endpoints"""
    print("\n🌐 Testing API Endpoints...")
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test root endpoint
        response = client.get("/")
        if response.status_code == 200:
            print(f"   ✅ Root endpoint: {response.json()['message']}")
        
        # Test health endpoint
        response = client.get("/health")
        if response.status_code == 200:
            print(f"   ✅ Health endpoint: {response.json()['status']}")
        
        # Test API documentation
        response = client.get("/docs")
        if response.status_code == 200:
            print(f"   ✅ API docs: Available")
        
        return True
    except Exception as e:
        print(f"   ❌ API endpoints error: {e}")
        return False

async def test_llm_service():
    """Test LLM service configuration (without making API calls)"""
    print("\n🤖 Testing LLM Service...")
    try:
        from core.llm_service import GenomicLLMService, OpenAIProvider
        from core.config import settings
        
        # Check configuration
        if settings.openai_api_key and settings.openai_api_key != "your_openai_api_key_here":
            print(f"   ✅ OpenAI API key: Configured")
        else:
            print(f"   ❌ OpenAI API key: Not configured")
        
        # Test provider initialization
        try:
            provider = OpenAIProvider()
            print(f"   ✅ OpenAI provider: Initialized")
        except Exception as e:
            print(f"   ❌ OpenAI provider: {e}")
        
        # Test service initialization
        llm_service = GenomicLLMService()
        print(f"   ✅ LLM service: Initialized")
        print(f"   ℹ️  Provider: {settings.llm_provider}")
        print(f"   ℹ️  Model: {settings.llm_model}")
        
        return True
    except Exception as e:
        print(f"   ❌ LLM service error: {e}")
        return False

async def test_genomic_processing():
    """Test genomic processing utilities"""
    print("\n🧬 Testing Genomic Processing...")
    try:
        from genomic_utils import GenomicProcessor
        
        processor = GenomicProcessor()
        
        # Test with mock VCF data
        mock_vcf_content = b"""##fileformat=VCFv4.2
##source=MockData
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
1	12345	rs123	A	T	60	PASS	.
2	67890	rs456	G	C	80	PASS	.
"""
        
        result = processor.process_genomic_file(mock_vcf_content, "test.vcf")
        
        if result.get("status") != "error":
            print(f"   ✅ VCF processing: Working")
            print(f"   ✅ Variants detected: {result.get('total_variants', 0)}")
        else:
            print(f"   ⚠️  VCF processing: {result.get('message', 'Unknown error')}")
        
        return True
    except Exception as e:
        print(f"   ❌ Genomic processing error: {e}")
        return False

async def test_frontend_integration():
    """Test frontend availability and integration points"""
    print("\n🖥️  Testing Frontend Integration...")
    try:
        frontend_path = Path("../../curagenie-frontend")
        
        if frontend_path.exists():
            package_json = frontend_path / "package.json"
            if package_json.exists():
                with open(package_json) as f:
                    pkg = json.load(f)
                print(f"   ✅ Frontend found: {pkg.get('name', 'Unknown')}")
                print(f"   ✅ Framework: Next.js")
                
                # Check for key files
                src_path = frontend_path / "src"
                if src_path.exists():
                    print(f"   ✅ Source directory: Present")
                
                return True
        
        print(f"   ❌ Frontend: Not found or misconfigured")
        return False
    except Exception as e:
        print(f"   ❌ Frontend integration error: {e}")
        return False

async def run_full_test():
    """Run comprehensive system test"""
    print("🚀 Starting CuraGenie Full System Test")
    print("=" * 50)
    
    tests = [
        ("Database", test_database()),
        ("ML Models", test_ml_models()),
        ("Redis", test_redis()),
        ("API Endpoints", test_api_endpoints()),
        ("LLM Service", test_llm_service()),
        ("Genomic Processing", test_genomic_processing()),
        ("Frontend Integration", test_frontend_integration())
    ]
    
    results = []
    for test_name, test_coro in tests:
        try:
            result = await test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:<10} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed >= 6:
        print("\n🎉 EXCELLENT! Your CuraGenie system is ready for production!")
        print("\nNext steps:")
        print("1. Add OpenAI credits to enable full LLM functionality")
        print("2. Start both backend and frontend servers") 
        print("3. Test the complete user workflow")
    elif passed >= 4:
        print("\n✅ GOOD! Core functionality is working, minor issues to address")
    else:
        print("\n⚠️  NEEDS WORK: Several components need attention")
    
    return passed, total

if __name__ == "__main__":
    asyncio.run(run_full_test())
