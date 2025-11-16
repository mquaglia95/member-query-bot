from fastapi import FastAPI
from pydantic import BaseModel
from app.qa import answer_question

app = FastAPI(title="Member Query Bot API")

class Question(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Member Query Bot API is running. Use POST /ask to query."}

@app.post("/ask")
async def ask_question(q: Question):
    answer = answer_question(q.question)
    return {"question": q.question, "answer": answer}