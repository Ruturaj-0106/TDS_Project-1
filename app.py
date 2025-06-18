
from fastapi import FastAPI, Request
from pydantic import BaseModel
from qa_model import get_answer

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: str = None

@app.post("/")
async def ask_question(request: QuestionRequest):
    answer, links = get_answer(request.question)
    return {
        "answer": answer,
        "links": links
    }
