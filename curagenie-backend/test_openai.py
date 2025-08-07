#!/usr/bin/env python3
"""
Test OpenAI API Key and Connection
"""

import openai
from core.config import settings

def test_openai_api():
    print('🔑 Testing OpenAI API Key...')
    
    # Check if API key is configured
    has_key = bool(settings.openai_api_key and settings.openai_api_key != "your_openai_api_key_here")
    print(f'API Key configured: {"✅ YES" if has_key else "❌ NO"}')
    
    if not has_key:
        print('❌ Please set your OpenAI API key in the .env file')
        return False
    
    # Test API connection
    try:
        client = openai.OpenAI(api_key=settings.openai_api_key)
        
        print('🚀 Testing API connection...')
        
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'user', 'content': 'Hello! Just testing the API connection. Respond with just: API WORKING'}
            ],
            max_tokens=10,
            temperature=0
        )
        
        print('✅ OpenAI API: WORKING!')
        print(f'✅ Response: {response.choices[0].message.content.strip()}')
        print('💰 Credits: Available and working')
        print('🎉 Your LLM integration is ready!')
        
        return True
        
    except openai.RateLimitError as e:
        print('❌ OpenAI API: Rate limit exceeded')
        print('💰 Credits: Insufficient or quota exceeded')
        print('💡 Solution: Add credits to your OpenAI account')
        print(f'Error details: {e}')
        return False
        
    except openai.AuthenticationError as e:
        print('❌ OpenAI API: Authentication failed')
        print('🔑 API Key: Invalid or incorrect')
        print('💡 Solution: Check your API key in .env file')
        print(f'Error details: {e}')
        return False
        
    except openai.BadRequestError as e:
        print('❌ OpenAI API: Bad request')
        print(f'Error details: {e}')
        return False
        
    except Exception as e:
        print(f'❌ OpenAI API: Unexpected error')
        print(f'Error details: {e}')
        return False

if __name__ == "__main__":
    success = test_openai_api()
    
    if success:
        print('\n🎯 READY TO TEST FULL CHATBOT!')
        print('Run: python -c "import asyncio; from core.llm_service import GenomicLLMService; llm = GenomicLLMService(); response = asyncio.run(llm.generate_response(\'user123\', \'What can you tell me about genetic risk?\')); print(response)"')
    else:
        print('\n❌ Fix the API key issue first, then try again')
