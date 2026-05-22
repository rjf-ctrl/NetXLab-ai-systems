from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
import time 
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY not found in environment. Check your .env file.")

def invoke_with_retry(model, prompt, retries=3, wait=50):
    for attempt in range(retries):
        try:
            return model.invoke(prompt)
        except Exception as e:
            if "429" in str(e) and attempt <retries - 1:
                logger.warning(f"Rate limited. Waiting {wait}s before retry {attempt + 1}...")
                time.sleep(wait)
            else:
                logger.error(f"Error invoking model: {e}")
                raise



flash_model = ChatGroq(model="llama-3.1-8b-instant", api_key=api_key)
pro_model =  ChatGroq(model="llama-3.1-8b-versatile", api_key=api_key)

app = FastAPI()

class TravelRequest(BaseModel):
    destination: str
    travel_dates: str
    preferences: str




@app.get("/")
def home():
    return {"message": "Travel API is running!"}


@app.post("/travel-assistant")
def travel_assistant(request: TravelRequest):

    try:
        prompt1 = f"You are an experienced Travel Guide with 5 star rating. Make a detailed travel itinerary for  a trip to {request.destination} from {request.travel_dates} .  Their preferences are {request.preferences}.Include recommendations for activities, accommodations, and dining options."
        prompt2= f"No fluff be conciseMake a detailed travel itinerary for  a trip to {request.destination} from {request.travel_dates} . Their preferences are {request.preferences}. Include recommendations for activities, accommodations, and dining options."
        
        flash_start = time.time()
        response_flash =invoke_with_retry(flash_model, prompt1)
        flash_latency = round((time.time() - flash_start)*1000, 2)

        pro_start = time.time()
        response_pro =invoke_with_retry(pro_model, prompt2)
        pro_latency = round((time.time() - pro_start)*1000, 2)

        faster = "Flash" if flash_latency < pro_latency else "Pro"
        summary = f"Flash responded in {flash_latency}ms, Pro responded in {pro_latency}ms. {faster} was faster."


        return {
        "trip_details": {
            "destination": request.destination,
            "travel_dates": request.travel_dates,
            "preferences": request.preferences
        },
        "flash_response": response_flash.content,
        "pro_response": response_pro.content,
        "comparison": {
            "flash_latency_ms": flash_latency,
            "pro_latency_ms": pro_latency,
            "summary": summary
        }
        }
    except Exception as e:
        logger.error(f"Error processing travel request: {e}")
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")
    

if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "8000"))
    uvicorn.run(app, host="127.0.0.1", port=port)


