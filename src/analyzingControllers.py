from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from audio_analyzer import AudioAnalyzer
import tempfile

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = AudioAnalyzer()

@app.post("/analyze-audio")
async def analyze_audio_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    metrics = analyzer.analyze_audio(tmp_path)
    return {"transcription": metrics.transcription}