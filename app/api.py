from fastapi import FastAPI, HTTPException
from app.models import ChatRequest
from app.chatbot import process_question


app = FastAPI()

@app.get("/")
def root():
    return {"message": "API Running"}

@app.post("/chat")
def process(request: ChatRequest):
    return process_question(request.question)

