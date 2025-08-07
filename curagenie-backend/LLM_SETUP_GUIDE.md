# CuraGenie LLM Integration Setup Guide

## Overview
The CuraGenie chatbot now supports real LLM integration with multiple providers:
- **OpenAI GPT** (Recommended for production)
- **Anthropic Claude** (Alternative premium option)
- **Local Ollama** (For local/offline deployment)

## Quick Start

### 1. Configure Environment Variables
Edit `curagenie-backend/.env` and add your API keys:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
```

### 2. Install Dependencies
```bash
cd curagenie-backend
pip install -r requirements.txt
```

### 3. Start the Backend
```bash
cd curagenie-backend
python main.py
```

### 4. Start the Frontend
```bash
cd curagenie-frontend
npm run dev
```

## Provider-Specific Setup

### OpenAI Setup (Recommended)
1. Create an account at [OpenAI](https://openai.com/)
2. Get your API key from the dashboard
3. Set in `.env`:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-3.5-turbo
   ```

**Models available:**
- `gpt-3.5-turbo` (Fast, cost-effective)
- `gpt-4` (Better quality, more expensive)
- `gpt-4-turbo` (Latest, balanced)

### Anthropic Claude Setup
1. Create an account at [Anthropic](https://console.anthropic.com/)
2. Get your API key
3. Set in `.env`:
   ```env
   ANTHROPIC_API_KEY=your-anthropic-key-here
   LLM_PROVIDER=anthropic
   ```

### Local Ollama Setup (Free)
1. Install [Ollama](https://ollama.ai/)
2. Start Ollama: `ollama serve`
3. Pull a model: `ollama pull llama2`
4. Set in `.env`:
   ```env
   LLM_PROVIDER=ollama
   LLM_MODEL=llama2
   OLLAMA_BASE_URL=http://localhost:11434
   ```

## Testing the Integration

### 1. Check Backend Health
Visit: `http://localhost:8000/api/chatbot/health`

Expected response:
```json
{
  "status": "healthy",
  "llm_provider": "OpenAIProvider",
  "provider_working": true,
  "features": {
    "genomic_context": true,
    "prs_integration": true,
    "variant_explanation": true,
    "personalized_recommendations": true
  }
}
```

### 2. Test API Directly
```bash
curl -X POST "http://localhost:8000/api/chatbot/chat" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test123", "message": "What are my PRS scores?"}'
```

### 3. Test Frontend
1. Go to: `http://localhost:3000/dashboard/chatbot`
2. Ask questions like:
   - "What are my PRS scores?"
   - "Explain my genetic risk for diabetes"
   - "What recommendations do you have for me?"

## Features

### Real Genomic Context
The chatbot automatically:
- Fetches user's PRS scores from the database
- Analyzes genetic variants
- Provides personalized recommendations
- Explains complex genetic concepts in simple terms

### Conversation Examples
**User:** "What does my diabetes risk mean?"
**AI:** "Based on your polygenic risk score of 0.73 (73rd percentile), you have an elevated genetic risk for Type 2 diabetes. However, this doesn't mean you'll definitely develop diabetes - it's about probability, not destiny. Your genetics account for about 40-70% of diabetes risk, with lifestyle factors playing a crucial role..."

## Troubleshooting

### Common Issues

1. **"LLM provider not working"**
   - Check API key is valid
   - Verify internet connection
   - Check rate limits

2. **"CORS errors"**
   - Ensure backend is running on port 8000
   - Check CORS_ORIGINS in .env

3. **"No genomic data"**
   - Upload sample genomic data first
   - Check database connection

### Fallback Mode
If no LLM provider works, the system automatically falls back to intelligent mock responses based on genomic data.

## Cost Optimization

### OpenAI Costs
- GPT-3.5-turbo: ~$0.002/1K tokens
- GPT-4: ~$0.03/1K tokens
- Average conversation: 500-1000 tokens
- Daily cost for active user: $0.05-$0.50

### Tips to Reduce Costs
1. Use GPT-3.5-turbo for most queries
2. Set max_tokens limit (currently 500)
3. Implement response caching
4. Use Ollama for development

## Production Deployment

### Security
- Never commit API keys to git
- Use environment variables or secrets manager
- Implement rate limiting
- Add user authentication

### Monitoring
- Monitor API usage and costs
- Log conversations for quality improvement
- Track response times and errors
- Implement health checks

### Scaling
- Use connection pooling
- Implement response caching
- Consider async processing for long queries
- Set up load balancing

## Advanced Configuration

### Custom Prompts
Edit `curagenie-backend/core/llm_service.py` to customize the system prompt for your specific needs.

### Adding New Providers
Extend the `LLMProvider` base class to add support for other LLM services like:
- Azure OpenAI
- AWS Bedrock
- Google PaLM
- Local models via Hugging Face

### Response Streaming
For real-time typing effects, implement streaming responses by modifying the provider implementations.

## Support
For issues or questions:
1. Check the logs in `curagenie-backend`
2. Test the `/health` endpoint
3. Verify your API keys are working
4. Check the FastAPI docs at `/docs`
