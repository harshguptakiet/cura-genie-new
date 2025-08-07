#!/usr/bin/env python3
"""
CuraGenie System Startup Script
Launches both backend and frontend servers
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting CuraGenie Backend...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "test_server.py"
        ], cwd=Path.cwd())
        
        print("   ✅ Backend starting on http://localhost:8000")
        print("   📖 API docs: http://localhost:8000/docs")
        return backend_process
    except Exception as e:
        print(f"   ❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Next.js frontend server"""
    print("\n🌐 Starting CuraGenie Frontend...")
    try:
        frontend_dir = Path("../../curagenie-frontend")
        
        if not frontend_dir.exists():
            print("   ❌ Frontend directory not found")
            return None
        
        # Check if npm is available
        npm_check = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if npm_check.returncode != 0:
            print("   ❌ npm not found - install Node.js first")
            return None
        
        # Start frontend dev server
        frontend_process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd=frontend_dir)
        
        print("   ✅ Frontend starting on http://localhost:3000")
        return frontend_process
    except Exception as e:
        print(f"   ❌ Failed to start frontend: {e}")
        return None

def main():
    print("🎯 CuraGenie System Launcher")
    print("=" * 50)
    
    # Start backend
    backend = start_backend()
    if not backend:
        print("❌ Cannot continue without backend")
        return
    
    # Wait a moment for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend
    frontend = start_frontend()
    
    if frontend:
        print("\n✅ Both servers starting!")
        print("=" * 50)
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("=" * 50)
        print("\n💡 Press Ctrl+C to stop both servers")
        
        try:
            # Keep both processes running
            while True:
                time.sleep(1)
                
                # Check if processes are still alive
                if backend.poll() is not None:
                    print("⚠️  Backend process ended")
                    break
                    
                if frontend.poll() is not None:
                    print("⚠️  Frontend process ended")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            
            if backend:
                backend.terminate()
                backend.wait()
                print("   ✅ Backend stopped")
                
            if frontend:
                frontend.terminate()
                frontend.wait() 
                print("   ✅ Frontend stopped")
                
            print("👋 CuraGenie shutdown complete")
    
    else:
        print("\n⚠️  Starting backend only...")
        print("🔧 Backend API: http://localhost:8000")
        
        try:
            backend.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping backend...")
            backend.terminate()
            backend.wait()
            print("👋 Backend stopped")

if __name__ == "__main__":
    main()
