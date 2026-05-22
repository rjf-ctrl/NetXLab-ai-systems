# Setting up a Virtual Environment and Downloading Dependencies

Created a project-specific Python environment using:
```
python -m venv venv
```

This created an isolated Python setup inside the `venv/` folder.

Activated it using:
```
source venv/bin/activate
```

This changed the current terminal session to use the environment’s Python and pip instead of the system-wide installation.

Verified it using:
```
which python
```

which returned the path to `venv/bin/python`.


installing project deepndecies: FastAPI, LangChain, Gemini Integration
```
pip install fastapi uvicorn langchain langchain-google-genai python-dotenv
```

here dependencies, bring in dependencies -> dependency trees. those pckages are also installed

Now List all installed packages and exact versions using:
```
pip freeze > requirements.txt
```
now someone can replicate the same environement with 
```
pip install -r requirements.txt
```

# Creating the FastAPI Application

create ```main.py``` : this is the entrypoint ie, execution starts here


```
from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Travel API is running!"}
```

build the smallest FastAPI app. import fastAPI libraries -> initialise a FastAPI application object 'app' -> if a request is made to "/", run the following code. A homepage ofmsorts
home is the handler for "/"

# Running the FastAPI server

Started the backend server using:

```
uvicorn main:app --reload
``` 

Here, `main:app` tells Uvicorn to import the `app` object from `main.py`, while `--reload` enables automatic server restart whenever code changes are detected.

Uvicorn started a long-running server process on:

```
http://127.0.0.1:8000
```

where `127.0.0.1` refers to the local machine and `8000` is the port the application is listening on.

The server now continuously waits for incoming HTTP requests and routes them to the correct FastAPI endpoint functions.

# First GET and POST

Import pydantic. It structues data into python compatible and validates and raises error if incoming or outgoing data does not meet schema. Automates validation in FastAPI.

```
from pydantic import BaseModel  
```

Make a POST, define  a schema to acccept data and use pydantic for validation

```
class TravelRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
```
this has TravelRequest inherit the methods of pudantic's BaseModel

```
@app.post("/travel-request")
def travel_assistant(request: TravelRequest):
    # Here you would implement the logic to process the travel request
    # For demonstration, we will just return the received data
    return {
        "message": "Travel request received!",
        "data": request.model_dump()
    }
```

so when client sends some data, FastAPI recieves raw JSON, sees parameter type as Travel request. lets Pydantic validate it and create an object so endpoint recieves structured object

**NOTE**: you can check the functioning of all ur api calls on http://127.0.0.1:8000/docs
**NOTE**: command-line program to sendHTTP requests: curl
eg: curl http://127.0.0.1:8000  sends a GET request to the server

# Connect Backent to AI

We need to build a prompt, send it to Gemini, receive AI reponse return it in JSON
You need API key so that gemini knows who is making the  requests

make .env file
and in it:
```
GOOGLE_API_KEY=your_key_here
```
**NOTE**:
NEVER:
commit API keys to GitHub
paste them publicly
hardcode them into source code
- Real developers treat API keys like passwords.
- There are real cases where leaked Gemini keys caused massive bills.

then add 
```
from dotenv import load_dotenv
import os
```

os is pythons built-in operating system module  taht lets pythin interact with files, environment variables, processes and pths

and 
```
load_dotenv()
```
this reads the .env file and loads the variables into the process environment, ie adds it to the environment varaibles of the process

now create a variable 
```
api_key = os.getenv("GOOGLE_API_KEY")
```

place this all before app so everythign can be loaded befre app is created

asks the operating system for a variable named GOOGLE_API_KEY - if found returns value else none. previously this was in system, now it gets added to process environment variables

**NOTE**: When `uvicorn main:app` runs, Uvicorn imports `main.py`, causing all top-level code in the file to execute automatically during startup. Functions themselves are not executed immediately — they are only registered with FastAPI and later called when matching HTTP requests arrive.

Langchain is a framework for building LLM-powered Applications. It handles authentication, request frmatting, model configs, responses, retries. (Software Layer)

```
from langchain_google_genai import ChatGoogleGenerativeAI
```

make an object: a configured Gemini Client tied to a specific model and authenticated w ur api_key

```
flash_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
```

# Create and submit a prompt

```
prompt = f"Make a detailed travel itinerary for  a trip to {request.destination} from {request.start_date} to {request.end_date} with a budget of {request.budget}. Include recommendations for activities, accommodations, and dining options."

response = flash_model.invoke(prompt)
```

.invoke() is a LangChain abstraction for:*execute this model call*
Underneath, it:formats request, authenticates, sends HTTP request to Gemini, waits for inference, receives response, converts it into Python object

now return the response in the POST

```
@app.post("/travel-request")
def travel_assistant(request: TravelRequest):

    prompt = f" Make a detailed travel itinerary for  a trip to {request.destination} from {request.start_date} to {request.end_date} with a budget of {request.budget}. Include recommendations for activities, accommodations, and dining options."
    
    response = flash_model.invoke(prompt)

    return {
    "trip_details": {
        "destination": request.destination,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "budget": request.budget
    },
    "ai_response": response.content
    }
```
**NOTE**: when testing, dont put commas in the number (eg. 40,000). json will interpret this ad 40 and 000 a saprate obj

repeate the process and instantiate the pro model as well. (since i dint wanna set up billing i used flah itself with a diff prompt)

# Comparing Model Responses

```
import time
```
to keep track of latency, right now i took a simple criterion of which one gives the faster response

```
flash_start = time.time()
    response_flash =flash_model.invoke(prompt)
    flash_latency = round((time.time() - flash_start)*1000, 2)

    pro_start = time.time()
    response_pro = pro_model.invoke(prompt)
    pro_latency = round((time.time() - pro_start)*1000, 2)

    faster = "Flash" if flash_latency < pro_latency else "Pro"
    summary = f"Flash responded in {flash_latency}ms, Pro responded in {pro_latency}ms. {faster} was faster."
```

time.time() records time at the moment that line is excuted.. so helps calculate execution times

# Error Handling
```
from fastapi import FastAPI, HTTPException
import logging
```
instantiate logger. its a more sophisticated error-handling-friendly version of print

```
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

```
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not found in environment. Check your .env file.")
```

make it so that a failure of the model dont just crash but instad elegantly returns error message instead of a lot of python messages which can also be a security problem

```

@app.post("/travel-request")
def travel_assistant(request: TravelRequest):

    try:
        prompt = f"You are an experienced Travel Guide with 5 star rating. Make a detailed travel itinerary for  a trip to {request.destination} from {request.travel_date} .  Their preferences are {request.preferences}.Include recommendations for activities, accommodations, and dining options."
        prompt = f"No fluff be conciseMake a detailed travel itinerary for  a trip to {request.destination} from {request.travel_date} . Their preferences are {request.preferences}. Include recommendations for activities, accommodations, and dining options."
        
        flash_start = time.time()
        response_flash =invoke_with_retry(flash_model, prompt)
        flash_latency = round((time.time() - flash_start)*1000, 2)

        pro_start = time.time()
        response_pro =invoke_with_retry(pro_model, prompt)
        pro_latency = round((time.time() - pro_start)*1000, 2)

        faster = "Flash" if flash_latency < pro_latency else "Pro"
        summary = f"Flash responded in {flash_latency}ms, Pro responded in {pro_latency}ms. {faster} was faster."


        return {
        "trip_details": {
            "destination": request.destination,
            "travel_date": request.travel_date,
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

```

# Environment-based config
Right now port is hardcoded/ default. The test script reads API_PORT from .env. 
```
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("API_PORT"))
    uvicorn.run(app, host="127.0.0.1", port=port)
```

if __name__ == "__main__": block is always the very last thing in the file — it's the "start everything" trigger, and everything needs to be defined before you pull that trigger.
This means you can run python main.py directly instead of the uvicorn command, and the port is controlled by .env.

`__name__` is a special Python variable automatically created for every file/module. If a file is run directly, `__name__` becomes `"__main__"`, but if the file is imported, it becomes the module’s filename instead.

When Python imports a file, it executes all top-level code inside that file automatically. Without `if __name__ == "__main__":`, the `uvicorn.run()` line would execute even when Uvicorn imports `main.py`, causing the server to try starting itself repeatedly. The `__main__` check ensures the startup code only runs when the file is executed directly using `python main.py`. This separates reusable code (functions/classes/app) from startup behavior.

# Rate Limiting/ Retries

```
def invoke_with_retry(model, prompt, retries=3, wait=30):
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
```

use this instead of just invoke
```
response_flash = invoke_with_retry(flash_model, prompt)
```

# Google API paywall
 Since it turned out that Google API was paywalled, I ended up switching to GroqAPI so i changed the API key in the .env and changed the model, pip installed langchain_groq and use llama instant and versatile and compared the two instead
- But kept all the variable names the same to pass the test script

 

