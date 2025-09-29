from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from question_generator import QuestionGenerator # your function
from models import PresentationMode

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = QuestionGenerator()

@app.post("/generate-questions")
async def generate_questions_endpoint(request: Request):
    data = await request.json()
    transcript = data.get("transcript", "")
    topic = data.get("topic", "")
    mode = PresentationMode(data.get("mode", "professional"))
    expert_documents = data.get("expert_documents", None)
    questions = await generator.generate_questions(transcript, topic, mode, expert_documents)
    return {"questions": [q.dict() for q in questions]}