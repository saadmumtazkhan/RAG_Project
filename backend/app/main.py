from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel

from app.retriever import retrieve_docs
from app.rag_chain import get_answer


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(req: QueryRequest):

    docs = retrieve_docs(req.question)

    answer = get_answer(req.question, docs)

    return {
        "question": req.question,
        "answer": answer
    }
