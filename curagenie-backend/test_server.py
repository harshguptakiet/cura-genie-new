#!/usr/bin/env python3
"""
Test server script for CuraGenie backend
"""
import logging
import uvicorn
from main import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("🚀 Starting CuraGenie test server...")
    logger.info("📊 Database: SQLite (curagenie.db)")
    logger.info("🌐 Server will be available at: http://localhost:8000")
    logger.info("📖 API Documentation: http://localhost:8000/docs")
    logger.info("⚡ Health check: http://localhost:8000/health")
    
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",  # Localhost only for security
            port=8000,
            reload=False,  # Disable reload for this test
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
