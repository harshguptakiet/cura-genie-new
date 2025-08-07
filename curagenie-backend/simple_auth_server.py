#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from db.database import Base, engine
from api.auth import router as auth_router

# Create FastAPI app
app = FastAPI(title="CuraGenie Auth Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include auth router
app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "auth-only"}

@app.get("/")
def root():
    return {"message": "CuraGenie Auth Server", "docs": "/docs"}

if __name__ == "__main__":
    print("🚀 Starting CuraGenie Auth Server...")
    print("📋 Available endpoints:")
    print("   - Health: http://localhost:8000/health")
    print("   - Login: http://localhost:8000/api/auth/login")
    print("   - Register: http://localhost:8000/api/auth/register")
    print("   - Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
