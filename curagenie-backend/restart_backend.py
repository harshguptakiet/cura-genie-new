#!/usr/bin/env python3
"""
Script to restart the backend server
"""
import subprocess
import sys
import time
import requests

def check_server_running():
    """Check if server is running"""
    try:
        response = requests.get('http://127.0.0.1:8000/health', timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    print("🔄 Restarting CuraGenie Backend Server...")
    
    if check_server_running():
        print("⚠️  Server is currently running. Please stop it first (Ctrl+C in the server terminal)")
        print("Then run this script again or manually start with: python main.py")
        return
    
    print("🚀 Starting backend server...")
    try:
        # Start the server
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

if __name__ == "__main__":
    main()
