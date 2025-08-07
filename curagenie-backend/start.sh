#!/bin/bash
# Simple startup script for Railway deployment

# Set default port if not provided
export PORT=${PORT:-8000}

echo "Starting CuraGenie API on port $PORT"

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port $PORT
