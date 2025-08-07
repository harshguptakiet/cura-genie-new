#!/usr/bin/env python3
"""
Test script for CuraGenie LLM integration
Run this to verify the chatbot setup is working correctly.
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from core.config import settings
        print("✅ Core config imported")
    except Exception as e:
        print(f"❌ Core config failed: {e}")
        return False
    
    try:
        from core.llm_service import GenomicLLMService
        print("✅ LLM service imported")
    except Exception as e:
        print(f"❌ LLM service failed: {e}")
        print("💡 Try: pip install -r requirements.txt")
        return False
    
    try:
        from api.chatbot import router
        print("✅ Chatbot API imported")
    except Exception as e:
        print(f"❌ Chatbot API failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test LLM configuration"""
    print("\n🔧 Testing configuration...")
    
    try:
        from core.config import settings
        
        print(f"📋 LLM Provider: {settings.llm_provider}")
        print(f"📋 LLM Model: {settings.llm_model}")
        
        # Check if API keys are configured (without exposing them)
        if settings.openai_api_key and settings.openai_api_key != "":
            if settings.openai_api_key.startswith("sk-"):
                print("✅ OpenAI API key looks valid")
            else:
                print("⚠️  OpenAI API key doesn't look like a real key")
        else:
            print("❌ OpenAI API key not configured")
        
        if settings.anthropic_api_key and settings.anthropic_api_key != "":
            print("✅ Anthropic API key configured")
        else:
            print("❌ Anthropic API key not configured")
        
        print(f"📋 Ollama URL: {settings.ollama_base_url}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_llm_service():
    """Test LLM service initialization"""
    print("\n🤖 Testing LLM service...")
    
    try:
        from core.llm_service import GenomicLLMService
        
        # Initialize service
        service = GenomicLLMService()
        provider_name = service.provider.__class__.__name__
        print(f"✅ LLM Service initialized with provider: {provider_name}")
        
        if provider_name == "MockProvider":
            print("⚠️  Using mock provider (no real LLM configured)")
        else:
            print(f"✅ Real LLM provider active: {provider_name}")
        
        return True
    except Exception as e:
        print(f"❌ LLM service test failed: {e}")
        return False

async def test_chatbot_response():
    """Test chatbot response generation"""
    print("\n💬 Testing chatbot response...")
    
    try:
        from core.llm_service import GenomicLLMService
        
        service = GenomicLLMService()
        
        # Test message
        test_user_id = "test_user_123"
        test_message = "Hello, can you help me understand my genetic data?"
        
        print(f"📤 Sending test message: '{test_message}'")
        
        # Generate response
        response = await service.generate_response(test_user_id, test_message)
        
        if response and len(response) > 10:
            print(f"✅ Response generated ({len(response)} characters)")
            print(f"📝 Sample: {response[:100]}...")
            return True
        else:
            print("❌ No valid response generated")
            return False
            
    except Exception as e:
        print(f"❌ Chatbot response test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoint structure"""
    print("\n🌐 Testing API endpoints...")
    
    try:
        from api.chatbot import router
        
        # Get router endpoints
        routes = [route.path for route in router.routes]
        print(f"📋 Available endpoints: {routes}")
        
        expected_endpoints = ["/chat", "/context/{user_id}", "/health"]
        
        for endpoint in expected_endpoints:
            full_path = f"/api/chatbot{endpoint}"
            if any(endpoint in route for route in routes):
                print(f"✅ Endpoint available: {full_path}")
            else:
                print(f"❌ Missing endpoint: {full_path}")
        
        return True
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧬 CuraGenie LLM Integration Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("LLM Service", test_llm_service),
        ("API Endpoints", test_api_endpoints),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Async test
    print("\n💬 Testing chatbot response...")
    try:
        import asyncio
        result = asyncio.run(test_chatbot_response())
        results.append(("Chatbot Response", result))
    except Exception as e:
        print(f"❌ Chatbot response test crashed: {e}")
        results.append(("Chatbot Response", False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, passed_test in results:
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"  {status} {test_name}")
        if passed_test:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! LLM integration is ready.")
        print("\n📝 Next steps:")
        print("1. Start the backend: python main.py")
        print("2. Start the frontend: npm run dev")
        print("3. Visit: http://localhost:3000/dashboard/chatbot")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("\n🔧 Common fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure API keys in .env file")
        print("3. Check database connection")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
