import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api import chatbot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CuraGenie Chatbot API",
    description="AI-Driven Genomics Chatbot",
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

# Include chatbot API router
app.include_router(chatbot.router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "CuraGenie Chatbot API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "chatbot_endpoints": [
            "/api/chatbot/chat",
            "/api/chatbot/health",
            "/api/chatbot/context/{user_id}"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "chatbot",
        "llm_provider": settings.llm_provider
    }

if __name__ == "__main__":
    print("🤖 Starting CuraGenie Chatbot API...")
    print(f"🔧 LLM Provider: {settings.llm_provider}")
    print(f"🔧 Model: {settings.llm_model}")
    print("📡 Server will start on: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("💬 Test endpoint: http://localhost:8000/api/chatbot/health")
    
    uvicorn.run(
        "chatbot_main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
