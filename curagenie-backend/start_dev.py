#!/usr/bin/env python3
"""
Development startup script for CuraGenie Backend

This script helps set up the development environment and provides
instructions for running all components.
"""

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required services are available"""
    print("🔍 Checking dependencies...")
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis is running")
    except Exception as e:
        print("❌ Redis is not running. Please start Redis server:")
        print("   - Windows: Download and run Redis")
        print("   - macOS: brew install redis && brew services start redis")
        print("   - Linux: sudo apt-get install redis-server")
        return False
    
    # Check PostgreSQL (attempt connection)
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            database="curagenie",
            user="postgres",
            password="password"
        )
        conn.close()
        print("✅ PostgreSQL is running and database exists")
    except Exception as e:
        print("❌ PostgreSQL connection failed:")
        print("   1. Install PostgreSQL")
        print("   2. Create database: CREATE DATABASE curagenie;")
        print("   3. Update .env with correct credentials")
        return False
    
    return True

def create_ml_model():
    """Create the ML model if it doesn't exist"""
    if not os.path.exists('models/diabetes_model.pkl'):
        print("🤖 Creating ML model...")
        try:
            subprocess.run([sys.executable, 'create_model.py'], check=True)
            print("✅ ML model created")
        except subprocess.CalledProcessError:
            print("❌ Failed to create ML model")
            return False
    else:
        print("✅ ML model already exists")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    print("🚀 CuraGenie Backend Development Setup")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check external services
    if not check_dependencies():
        print("\n❌ Please fix the dependency issues above before continuing.")
        return
    
    # Create ML model
    if not create_ml_model():
        return
    
    print("\n✅ Setup complete! You can now start the services:")
    print("\n🔧 To start the backend:")
    print("   python main.py")
    print("\n👷 To start the Celery worker:")
    print("   python worker/worker.py")
    print("\n🌐 API will be available at:")
    print("   - Main API: http://localhost:8000")
    print("   - Documentation: http://localhost:8000/docs")
    print("   - WebSocket: ws://localhost:8000/ws/{user_id}")
    
    print("\n📊 Monitor Celery tasks:")
    print("   celery -A core.celery_app flower")
    
    print("\n🧪 Test the API:")
    print("   curl http://localhost:8000/health")

if __name__ == "__main__":
    main()
