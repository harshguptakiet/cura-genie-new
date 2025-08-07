import uvicorn

if __name__ == "__main__":
    print("🤖 Starting CuraGenie Chatbot API on http://localhost:8000...")
    print("💬 Test your chatbot at: http://localhost:3000/dashboard/chatbot")
    print("📚 API docs at: http://localhost:8000/docs")
    print("🛑 Press CTRL+C to stop")
    
    uvicorn.run(
        "chatbot_main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload for stability
        log_level="info"
    )
