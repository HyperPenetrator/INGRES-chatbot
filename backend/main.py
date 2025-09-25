# main.py (Final Version for Render Deployment)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import csv

app = FastAPI()

# 1. CORS MIDDLEWARE
# This allows your Netlify frontend to talk to this Render backend.
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://sih-internal-hackathon-hack4nothing.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. LOAD DATASET
# --- FIX: Simplified the file path to work reliably on Render ---
datasets = {}
# Get the directory where this main.py file is located
current_dir = os.path.dirname(__file__)
# The 'data' folder is now inside the 'backend' folder, next to this file
data_dir = os.path.join(current_dir, "data") 
# --- END OF FIX ---

print(f"Attempting to load data from: {data_dir}")
if not os.path.exists(data_dir):
    print(f"FATAL ERROR: Data directory not found at {data_dir}")
else:
    for fname in os.listdir(data_dir):
        if fname.endswith(".csv"):
            state_key = fname.replace(".csv", "").lower()
            file_path = os.path.join(data_dir, fname)
            try:
                with open(file_path, "r", encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    datasets[state_key] = list(reader)
                    print(f"Successfully loaded {len(datasets[state_key])} rows from {fname}")
            except Exception as e:
                print(f"Error loading {fname}: {e}")

# 3. API ROUTE
@app.post("/chat")
async def handle_chat_request(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    normalized_message = user_message.lower()

    bot_response_text = ""
    bot_response_data = None

    if "andhra" in normalized_message:
        state_key = next((key for key in datasets if "andhra" in key), None)
        if state_key and datasets.get(state_key):
            bot_response_text = "Here is a sample of the groundwater data for Andhra Pradesh:"
            bot_response_data = datasets[state_key][:3]
        else:
            bot_response_text = "Sorry, data for Andhra Pradesh could not be found."

    elif "maharashtra" in normalized_message:
        state_key = next((key for key in datasets if "maharashtra" in key), None)
        if state_key and datasets.get(state_key):
            bot_response_text = "Here is a sample of the groundwater data for Maharashtra:"
            bot_response_data = datasets[state_key][:3]
        else:
            bot_response_text = "Sorry, data for Maharashtra could not be found."
    
    else:
        bot_response_text = "I'm sorry, I don't have information for that location."

    return {"response": bot_response_text, "data": bot_response_data}

