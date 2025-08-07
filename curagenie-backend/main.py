#!/usr/bin/env python3
"""
Ultra-minimal FastAPI app for Railway deployment
This is main.py to work with Railway's Python auto-detection
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CuraGenie API - Minimal",
    description="Minimal backend for testing deployment",
    version="1.0.0-minimal",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Simple CORS - allow your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cura-g.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CuraGenie Minimal API is running",
        "version": "1.0.0-minimal",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "curagenie-minimal-api",
        "version": "1.0.0"
    }

@app.post("/api/auth/login")
async def login():
    """Temporary login endpoint for testing"""
    return {
        "access_token": "temp-token-123",
        "token_type": "bearer",
        "user_id": 1,
        "role": "patient"
    }

@app.post("/api/auth/register")
async def register():
    """Temporary register endpoint for testing"""
    return {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "role": "patient"
    }

@app.get("/api/auth/me")
async def get_me():
    """Temporary user info endpoint"""
    return {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "role": "patient",
        "is_active": True,
        "is_verified": True
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
