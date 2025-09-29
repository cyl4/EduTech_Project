from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from openai import OpenAI
import tempfile
import os
import json
import uuid
from typing import List, Optional
from dotenv import load_dotenv
from src.presentation_analyzer import PresentationAnalyzer
from src.models import PresentationMode
import aiofiles
import PyPDF2
from io import BytesIO

load_dotenv()
client = OpenAI()

app = FastAPI(title="AI Presentation Coach", description="AI-powered presentation skills improvement")

# Initialize the presentation analyzer
analyzer = PresentationAnalyzer(client)

# Store active WebSocket connections
active_connections: dict = {}

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main application page"""
    try:
        with open("static/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Presentation Coach</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { text-align: center; margin-bottom: 40px; }
                .feature { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎤 AI Presentation Coach</h1>
                    <p>Improve your presentation skills with AI-powered feedback</p>
                </div>
                
                <div class="feature">
                    <h3>🎯 Real-time Analysis</h3>
                    <p>Get instant feedback on pace, tone, filler words, and clarity</p>
                </div>
                
                <div class="feature">
                    <h3>🧠 Adaptive Modes</h3>
                    <p>Choose from professional, technical, layperson, or casual presentation styles</p>
                </div>
                
                <div class="feature">
                    <h3>❓ Smart Questions</h3>
                    <p>AI generates relevant questions to test your understanding</p>
                </div>
                
                <div class="feature">
                    <h3>💡 Improvement Suggestions</h3>
                    <p>Get metaphors, analogies, and visual aids to improve unclear explanations</p>
                </div>
                
                <div class="feature">
                    <h3>📊 Comprehensive Scoring</h3>
                    <p>Detailed scoring system with actionable feedback</p>
                </div>
                
                <p><strong>Note:</strong> The web interface is being built. The backend API is ready for integration.</p>
            </div>
        </body>
        </html>
        """)

@app.post("/api/sessions")
async def create_session(
    mode: str = Form(...),
    topic: str = Form(...),
    custom_context: Optional[str] = Form(None)
):
    """Create a new presentation session"""
    try:
        presentation_mode = PresentationMode(mode)
        session_id = str(uuid.uuid4())
        
        session = analyzer.create_session(
            session_id=session_id,
            mode=presentation_mode,
            topic=topic,
            custom_context=custom_context
        )
        
        return {"session_id": session_id, "status": "created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/sessions/{session_id}/analyze-text")
async def analyze_text_only(session_id: str, transcript: str = Form(...)):
    """Analyze a transcript chunk without audio for quick testing."""
    session = analyzer.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Analyze content only; create empty audio metrics via zeroed bytes
    score = await analyzer.analyze_presentation_chunk(session_id, b"", transcript)
    return {"score": score.dict()}

@app.post("/api/sessions/{session_id}/expert-documents")
async def upload_expert_documents(
    session_id: str,
    files: List[UploadFile] = File(...)
):
    """Upload expert documents for technical mode"""
    try:
        session = analyzer.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        document_contents = []
        for file in files:
            if file.content_type == "application/pdf":
                content = await file.read()
                pdf_reader = PyPDF2.PdfReader(BytesIO(content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                document_contents.append(text)
            else:
                content = await file.read()
                document_contents.append(content.decode('utf-8'))
        
        session.expert_documents = document_contents
        return {"status": "documents uploaded", "count": len(document_contents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions/{session_id}/summary")
async def get_session_summary(session_id: str):
    """Get comprehensive session summary"""
    try:
        summary = analyzer.get_session_summary(session_id)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time presentation analysis"""
    await websocket.accept()
    active_connections[session_id] = websocket
    audio_buffer = b""
    
    try:
        while True:
            data = await websocket.receive_bytes()
            audio_buffer += data

            # Process every ~5 seconds of audio
            if len(audio_buffer) > 16000 * 2 * 5:  # 16kHz * 2 bytes * 5s
                with tempfile.NamedTemporaryFile(delete=True, suffix=".wav") as tmp:
                    tmp.write(audio_buffer)
                    tmp.flush()

                    # Transcribe audio
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=open(tmp.name, "rb")
                    )
                    
                    # Analyze presentation
                    score = await analyzer.analyze_presentation_chunk(
                        session_id, audio_buffer, transcript.text
                    )
                    
                    # Generate questions and suggestions
                    questions = await analyzer.generate_questions_for_session(
                        session_id, transcript.text
                    )
                    
                    suggestions = await analyzer.generate_suggestions_for_session(
                        session_id, transcript.text
                    )
                    
                    # Send comprehensive feedback
                    feedback = {
                        "transcript": transcript.text,
                        "score": score.dict(),
                        "questions": [q.dict() for q in questions[-3:]],  # Last 3 questions
                        "suggestions": [s.dict() for s in suggestions[-3:]]  # Last 3 suggestions
                    }
                    
                    await websocket.send_text(json.dumps(feedback))
                
                audio_buffer = b""  # Reset buffer

    except WebSocketDisconnect:
        if session_id in active_connections:
            del active_connections[session_id]
    except Exception as e:
        print(f"WebSocket error: {e}")
        if session_id in active_connections:
            del active_connections[session_id]

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a presentation session"""
    success = analyzer.delete_session(session_id)
    if success:
        return {"status": "deleted"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)