import logging
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.websockets import connection_manager
from db.database import create_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import APIs with error handling
ML_APIS_AVAILABLE = False
ENHANCED_MRI_AVAILABLE = False

# Always import core APIs first
try:
    from api import auth, profile, reports, local_upload
    logger.info("✅ Core APIs imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import core APIs: {e}")
    # Create minimal auth API if needed

# Try to import ML APIs
try:
    from api import genomic, prs, ml, chatbot, direct_prs, timeline, genomic_variants, mri_analysis
    ML_APIS_AVAILABLE = True
    logger.info("✅ ML APIs imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ ML APIs not available: {e}")
    ML_APIS_AVAILABLE = False

# Try to import enhanced MRI analysis
try:
    from api import enhanced_mri_analysis
    ENHANCED_MRI_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced MRI analysis not available: {e}")
    ENHANCED_MRI_AVAILABLE = False

# Create FastAPI app
app = FastAPI(
    title="CuraGenie API",
    description="AI-Driven Healthcare Genomics Platform Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers (always available)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(reports.router)
app.include_router(local_upload.router)

# Include ML APIs if available
if ML_APIS_AVAILABLE:
    app.include_router(genomic.router)
    app.include_router(prs.router)
    app.include_router(ml.router)
    app.include_router(chatbot.router)
    app.include_router(direct_prs.router)
    app.include_router(timeline.router)
    app.include_router(genomic_variants.router)
    app.include_router(mri_analysis.router)
    logger.info("✅ ML APIs loaded successfully")
else:
    logger.warning("⚠️ ML APIs not available - running in limited mode")

# Include enhanced MRI if available
if ENHANCED_MRI_AVAILABLE:
    app.include_router(enhanced_mri_analysis.router)
    logger.info("✅ Enhanced MRI analysis loaded")
else:
    logger.warning("⚠️ Enhanced MRI analysis not available")

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        create_tables()
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time updates"""
    await connection_manager.connect(websocket, user_id)
    try:
        while True:
            # Keep connection alive and listen for any messages from client
            data = await websocket.receive_text()
            logger.info(f"Received message from user {user_id}: {data}")
            
            # Echo back a response (optional)
            await connection_manager.send_personal_message(
                user_id,
                {
                    "event": "message_received",
                    "message": "Message received by server",
                    "original_message": data
                }
            )
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)
        logger.info(f"User {user_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        connection_manager.disconnect(user_id)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "CuraGenie API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "websocket": "/ws/{user_id}",
        "active_connections": connection_manager.get_active_connections_count()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_websocket_connections": connection_manager.get_active_connections_count(),
        "ml_apis_available": ML_APIS_AVAILABLE,
        "enhanced_mri_available": ENHANCED_MRI_AVAILABLE
    }

@app.get("/system/status")
async def system_status():
    """Detailed system status"""
    available_endpoints = []
    
    # Always available
    available_endpoints.extend([
        "POST /auth/register - User registration",
        "POST /auth/login - User login",
        "GET /profile - User profile",
        "GET /reports - Analysis reports",
        "POST /upload - File upload"
    ])
    
    if ML_APIS_AVAILABLE:
        available_endpoints.extend([
            "POST /api/mri/upload - MRI scan upload",
            "GET /api/mri/analysis/{id} - MRI analysis results",
            "POST /api/mri/test-real-analysis - Test MRI analysis",
            "POST /genomic/upload - Genomic file upload",
            "GET /prs/calculate - Polygenic risk scores",
            "POST /ml/predict - Machine learning predictions",
            "POST /chatbot/chat - AI chatbot"
        ])
    
    if ENHANCED_MRI_AVAILABLE:
        available_endpoints.extend([
            "POST /api/enhanced-mri/upload - Enhanced MRI analysis",
            "GET /api/enhanced-mri/test - Enhanced MRI test",
            "POST /api/enhanced-mri/test-cnn-analysis - CNN analysis test"
        ])
    
    return {
        "status": "operational",
        "modules": {
            "core_apis": True,
            "ml_apis": ML_APIS_AVAILABLE,
            "enhanced_mri": ENHANCED_MRI_AVAILABLE
        },
        "available_endpoints": available_endpoints,
        "brain_tumor_detection": ML_APIS_AVAILABLE,  # Your working MRI analysis
        "message": "CuraGenie Backend is running"
    }

@app.get("/ws/status")
async def websocket_status():
    """Get WebSocket connection status"""
    return {
        "active_connections": connection_manager.get_active_connections_count(),
        "connection_manager_status": "active"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
