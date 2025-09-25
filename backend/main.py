from fastapi import FastAPI
import os, json

app = FastAPI()

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
