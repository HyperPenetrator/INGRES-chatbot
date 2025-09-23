# main.py (with a debug print statement)

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os, csv

app = FastAPI()

# 1. ADD MIDDLEWARE FIRST
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load sample groundwater datasets ---
datasets = {}
data_dir = os.path.join(os.path.dirname(__file__), "../data")
for fname in os.listdir(data_dir):
    if fname.endswith(".csv"):
        state = fname.replace(".csv", "")
        try:
            with open(os.path.join(data_dir, fname), "r", encoding='utf-8') as f:
                reader = csv.DictReader(f)
                datasets[state] = list(reader)
        except Exception as e:
            print(f"Error loading {fname}: {e}")


# 2. DEFINE ALL API ROUTES NEXT
@app.post("/chat")
async def handle_chat_request(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    normalized_message = user_message.lower()

    bot_response_text = ""
    bot_response_data = None

    if "andhra" in normalized_message:
        state_key = next((key for key in datasets if "andhra" in key.lower()), None)
        if state_key:
            bot_response_text = f"Here is a sample of the groundwater data for Andhra Pradesh:"
            
            # --- THIS IS THE NEW DEBUGGING LINE ---
            print(f"DEBUG INFO: Found data for key '{state_key}'. Total rows loaded: {len(datasets[state_key])}")
            # --- END OF DEBUGGING LINE ---

            bot_response_data = datasets[state_key][:3]
        else:
            bot_response_text = "Sorry, data for Andhra Pradesh could not be found."

    elif "maharashtra" in normalized_message:
        state_key = next((key for key in datasets if "maharashtra" in key.lower()), None)
        if state_key:
            bot_response_text = f"Here is a sample of the groundwater data for Maharashtra:"
            
            # --- THIS IS THE NEW DEBUGGING LINE ---
            print(f"DEBUG INFO: Found data for key '{state_key}'. Total rows loaded: {len(datasets[state_key])}")
            # --- END OF DEBUGGING LINE ---
            
            bot_response_data = datasets[state_key][:3]
        else:
            bot_response_text = "Sorry, data for Maharashtra could not be found."
    
    else:
        bot_response_text = "I'm sorry, I don't have information for that location."

    return {"response": bot_response_text, "data": bot_response_data}


# 3. MOUNT STATIC FILES LAST
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
