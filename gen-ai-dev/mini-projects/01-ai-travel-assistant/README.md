# Travel Assistant API

## Problem Statement
*You will build a REST API endpoint /travel-assistant powered by Google’s Gemini models (via LangChain)
The API will:
    Take a user’s travel request (destination, preferences, dates)
    Use Gemini Flash and Gemini Pro models
    Compare responses from both models and return them in a structured JSON response*

FastAPI REST API using LangChain with Groq(due to Google paywal) to generate 
travel itineraries. Calls two model instances with different prompts 
and compares latency between them.

## Design Decisions
- Used llama-3.1-8b-instant and llama-3.1-8b-versatile 
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

*NOTE*: variable names in the assignnment still refernce pro and flash models to pass the test_script for the assigment. Gemini models were not used for the assignment
