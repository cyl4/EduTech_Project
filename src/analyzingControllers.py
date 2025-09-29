from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from audio_analyzer import analyze_audio  

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-audio")
async def analyze_audio_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    transcript = analyze_audio(audio_bytes)  # implement this in audio_analyzer.py
    return {"transcript": transcript}