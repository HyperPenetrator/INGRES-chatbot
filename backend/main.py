from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json

# --- Pydantic model for request body ---
# This defines the expected structure for the incoming message from the frontend.
class ChatMessage(BaseModel):
    message: str

app = FastAPI()

# --- CORS Configuration ---
# This remains the same to allow your frontend to connect.
origins = [
    "https://ingres-chatbot-2.onrender.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dataset Directory ---
DATASET_DIR = os.path.join(os.path.dirname(__file__), "../datasets")

# --- Helper function to load data ---
def load_dataset_by_name(name: str):
    """Loads a dataset JSON file based on a given name."""
    filepath = os.path.join(DATASET_DIR, f"{name}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None

# --- API Endpoints ---
@app.get("/")
def root():
    return {"message": "INGRES Chatbot Backend Running!"}

# --- NEW CHATBOT LOGIC ENDPOINT ---
@app.post("/chat")
def chat(chat_message: ChatMessage):
    """
    This is the main chatbot endpoint. It processes the user's message
    and returns a structured response with data.
    """
    user_message = chat_message.message.lower()
    
    # Simple keyword matching to determine which dataset to send
    if "andhra" in user_message:
        data = load_dataset_by_name("2023") # Assuming 2023.json is for Andhra Pradesh
        if data:
            return {
                "response": "Here is the groundwater data for Andhra Pradesh:",
                "data": data
            }
        else:
             return {"response": "Sorry, I couldn't find the dataset for Andhra Pradesh."}

    elif "maharashtra" in user_message:
        data = load_dataset_by_name("2022") # Assuming 2022.json is for Maharashtra
        if data:
            return {
                "response": "Here is the groundwater data for Maharashtra:",
                "data": data
            }
        else:
            return {"response": "Sorry, I couldn't find the dataset for Maharashtra."}

    # If no keywords are matched, return a default response
    return {
        "response": "I'm sorry, I can only provide data for 'Andhra Pradesh' or 'Maharashtra'. Please ask me about one of those."
    }

