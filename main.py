import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Nexus Prime Content API")

class TopicRequest(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"status": "online", "engine": "Nexus Prime Core"}

@app.post("/generate")
def generate_content(request: TopicRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
        
    try:
        # Render will pass the API key securely via environment variables
        client = genai.Client()
        
        prompt = (
            f"Act as a viral video copywriter. For the topic '{request.topic}', "
            "generate exactly 3 hooks: 1. Question Hook, 2. Negative Hook, and 3. Data Hook. "
            "Then, provide a structured 60-second video script structure layout."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return {"topic": request.topic, "production_blueprint": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
