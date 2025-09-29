from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from question_generator import generate_question  # your function

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-question")
async def generate_question_endpoint(request: Request):
    data = await request.json()
    question = data.get("question")
    answer = generate_question(question) 
    return {"answer": answer}