#!/usr/bin/env python3
"""
Quick status check for CuraGenie backend
"""

import os
import sys
from pathlib import Path

def check_status():
    status = {
        "database": False,
        "models": False,
        "redis": False,
        "config": False,
        "frontend": False
    }
    
    # Check database
    if os.path.exists("curagenie.db"):
        status["database"] = True
        db_size = os.path.getsize("curagenie.db") / 1024  # KB
        print(f"✅ Database: SQLite ready ({db_size:.1f} KB)")
    else:
        print("❌ Database: Missing")
    
    # Check models
    models_dir = Path("models")
    if models_dir.exists():
        model_files = list(models_dir.glob("*.pkl")) + list(models_dir.glob("*.h5"))
        if model_files:
            status["models"] = True
            print(f"✅ ML Models: {len(model_files)} files found")
            for model in model_files:
                size_mb = model.stat().st_size / 1024 / 1024
                print(f"   - {model.name} ({size_mb:.1f} MB)")
        else:
            print("❌ ML Models: No model files found")
    else:
        print("❌ ML Models: Directory missing")
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        status["redis"] = True
        print("✅ Redis: Connected")
    except Exception as e:
        print(f"❌ Redis: {e}")
    
    # Check config
    if os.path.exists(".env"):
        status["config"] = True
        print("✅ Configuration: .env file exists")
        
        # Check for API keys
        with open(".env", "r") as f:
            content = f.read()
            if "your_openai_api_key_here" in content:
                print("   ⚠️  OpenAI API key needs to be set")
            elif "OPENAI_API_KEY=sk-" in content:
                print("   ✅ OpenAI API key configured")
    else:
        print("❌ Configuration: .env file missing")
    
    # Check frontend
    frontend_path = Path("../../curagenie-frontend")
    if frontend_path.exists() and (frontend_path / "package.json").exists():
        status["frontend"] = True
        print("✅ Frontend: Next.js app found")
    else:
        print("❌ Frontend: Not found")
    
    # Overall status
    ready_count = sum(status.values())
    total_count = len(status)
    
    print(f"\n📊 Overall Status: {ready_count}/{total_count} components ready")
    
    if ready_count >= 4:
        print("🚀 System is ready for testing!")
        print("\nNext steps:")
        print("1. Set OpenAI API key in .env if needed")
        print("2. Run: python test_server.py")
        print("3. Test frontend integration")
    elif ready_count >= 2:
        print("⚠️  System partially ready - some components need attention")
    else:
        print("❌ System needs significant setup work")
    
    return status

if __name__ == "__main__":
    check_status()
