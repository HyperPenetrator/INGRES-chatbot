from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

origins = [
    "https://ingres-chatbot-2.onrender.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # List of origins allowed
    allow_credentials=True,      # Allow cookies
    allow_methods=["*"],         # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],         # Allow all headers
)

DATASET_DIR = os.path.join(os.path.dirname(__file__), "../datasets")

@app.get("/")
def root():
    return {"message": "INGRES Chatbot Backend Running!"}

@app.get("/datasets/{year}")
def get_dataset(year: str):
    filepath = os.path.join(DATASET_DIR, f"{year}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return {"error": f"Dataset for {year} not found"}
