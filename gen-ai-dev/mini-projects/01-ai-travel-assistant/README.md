# Travel Assistant API

## Approach
FastAPI REST API using LangChain with Gemini 2.5 Flash to generate 
travel itineraries. Calls two model instances with different prompts 
and compares latency between them.

## Design Decisions
- Used gemini-2.5-flash for both models due to free tier limitations on gemini-2.5-pro
- Added retry logic to handle rate limiting gracefully
- Added structured logging for latency tracking
- API key validated on startup to fail fast if misconfigured

## How to run
1. Add your GOOGLE_API_KEY and PORT to .env file
   ```
   GOOGLE_API_KEY=your_api_key
    API_PORT = your_port_no
   ```
2. pip install -r requirements.txt
3. python main.py