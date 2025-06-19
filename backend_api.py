from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from fastapi.middleware.cors import CORSMiddleware

from monopoly_chat import MonopolyRAGChat

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
chatbot = MonopolyRAGChat()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/ask", response_model=QueryResponse)
async def ask_question(req: QueryRequest):
    answer = await chatbot.get_response(req.question)
    return QueryResponse(answer=answer) 
