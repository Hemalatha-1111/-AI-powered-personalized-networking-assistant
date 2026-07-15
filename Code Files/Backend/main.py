from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from event_analyzer import extract_themes, generate_prompts # <-- changed this line
from fact_checker import verify_topic
from datetime import datetime

app = FastAPI(title="Personalized Networking Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HISTORY_FILE = "data/history.json"
FEEDBACK_FILE = "data/feedback.json"
os.makedirs("data", exist_ok=True)

class GenerateRequest(BaseModel):
    description: str
    interests: str

# class VerifyRequest(BaseModel):
    # topic: str

class FeedbackRequest(BaseModel):
    prompt: str
    feedback: str

def save_json(file_path, data):
    existing = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f: existing = json.load(f)
        except: existing = []
    existing.append(data)
    with open(file_path, "w") as f: json.dump(existing, f, indent=4)

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.post("/api/v1/generate")
def generate(req: GenerateRequest):
    # if not req.description:
        # raise HTTPException(status_code=400, detail="Description required")
    
    # Call functions directly, no class
    themes = extract_themes(req.description)
    main_theme = themes[0]
    prompts = generate_prompts(main_theme, req.interests)
    
    save_json(HISTORY_FILE, {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # date add
    "description": req.description,"theme": main_theme, "interests": req.interests, "prompts": prompts})
    return {"theme": main_theme, "themes": themes, "prompts": prompts}

@app.get("/api/v1/verify")
def verify(topic: str):
    return verify_topic(topic)

@app.post("/api/v1/feedback")
def feedback(req: FeedbackRequest):
    save_json(FEEDBACK_FILE, {"prompt": req.prompt, "feedback": req.feedback})
    return {"status": "Feedback recorded"}

@app.get("/api/v1/history")
def history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f: return json.load(f)
    return []

@app.post("/api/v1/generate")
def generate(req:GenerateRequest):
    themes=extract_themes(req.description)
    main_theme=themes[0]
    prompts=generate_prompts(main_theme,req.interests)

    save_json(HISTORY_FILE,{
        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "theme":main_theme,
        "interests":req.interests,
        "prompts":prompts 
    })
    return {"theme":main_theme,"themes":themes,"prompts":prompts  }