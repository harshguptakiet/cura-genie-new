#!/usr/bin/env python3
"""
ABSOLUTE MINIMAL test - just FastAPI with one endpoint
"""

from fastapi import FastAPI

app = FastAPI(title="Test API")

@app.get("/")
def read_root():
    return {"message": "Hello World", "status": "working"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/auth/login")
def fake_login():
    return {
        "access_token": "fake-token-123",
        "token_type": "bearer",
        "user_id": 1,
        "role": "patient"
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
