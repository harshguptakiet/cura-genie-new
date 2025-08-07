#!/usr/bin/env python3
"""
Simplified backend server for auth and timeline testing
Avoids heavy ML dependencies
"""
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CuraGenie Auth API",
    description="Simplified backend for auth and timeline testing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
try:
    from api.auth import router as auth_router
    from api.timeline import router as timeline_router
    from api.genomic_variants import router as genomic_router
    from db.database import create_tables
    
    # Include routers
    app.include_router(auth_router)
    app.include_router(timeline_router)
    app.include_router(genomic_router)
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize database tables on startup"""
        try:
            create_tables()
            logger.info("✅ Database tables created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create database tables: {e}")
            
except ImportError as e:
    logger.error(f"❌ Failed to import routers: {e}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "CuraGenie Simplified API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "/api/auth/login",
            "/api/auth/register", 
            "/api/timeline/{user_id}",
            "/api/genomic/variants/{user_id}"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "server": "simplified"
    }

if __name__ == "__main__":
    logger.info("🚀 Starting CuraGenie simplified auth server...")
    logger.info("📊 Database: SQLite (curagenie.db)")
    logger.info("🌐 Server will be available at: http://localhost:8000")
    logger.info("📖 API Documentation: http://localhost:8000/docs")
    logger.info("⚡ Health check: http://localhost:8000/health")
    
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
