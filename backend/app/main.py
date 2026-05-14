import logging
import re

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import MAX_QUESTION_LENGTH, MIN_QUESTION_LENGTH
from app.retriever import retrieve_docs
from app.rag_chain import get_answer
from app.validation import (
    build_context_from_chunks,
    parse_grounded_answer,
    public_retrieval_validation,
    validate_grounding,
    validate_retrieval,
)

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

GREETING_PATTERN = re.compile(
    r"^\s*(hi|hello|hey|thanks|thank you|good morning|good afternoon|good evening|what's up|how are you)\b",
    re.IGNORECASE,
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    # Request validation prevents empty or oversized prompts from reaching
    # retrieval and LLM layers.
    question: str = Field(
        min_length=MIN_QUESTION_LENGTH,
        max_length=MAX_QUESTION_LENGTH
    )


@app.post("/ask")
def ask_question(req: QueryRequest):

    if GREETING_PATTERN.match(req.question):
        return {
            "question": req.question,
            "answer": "Hi there! I can help with questions about this video's transcript.",
            "validation": {
                "retrieval": {
                    "is_valid": True,
                    "reason": "Greeting or small talk bypassed retrieval.",
                    "scores": [],
                    "chunks": [],
                },
                "grounding": {
                    "is_valid": True,
                    "reason": None,
                },
            },
            "token_usage": None,
        }

    docs_with_scores = retrieve_docs(req.question)
    retrieval = validate_retrieval(docs_with_scores)
    public_retrieval = public_retrieval_validation(retrieval)

    if not retrieval["is_valid"]:
        return {
            "question": req.question,
            "answer": "I could not find enough relevant transcript context to answer safely.",
            "validation": {
                "retrieval": public_retrieval,
                "grounding": None,
            },
            "token_usage": None,
        }

    context = build_context_from_chunks(retrieval["chunks"])
    llm_response = get_answer(req.question, context)

    usage = llm_response["usage"]

    # Token usage is logged per completed LLM request so costs and prompt size
    # can be monitored without changing the chat UI.
    logger.info(
        "llm_token_usage prompt_tokens=%s completion_tokens=%s total_tokens=%s",
        usage["prompt_tokens"] if usage else None,
        usage["completion_tokens"] if usage else None,
        usage["total_tokens"] if usage else None,
    )

    grounded_answer, parse_error = parse_grounded_answer(llm_response["content"])

    if parse_error:
        return {
            "question": req.question,
            "answer": "I could not validate the model response as grounded transcript output.",
            "validation": {
                "retrieval": public_retrieval,
                "grounding": {
                    "is_valid": False,
                    "reason": parse_error,
                },
            },
            "token_usage": usage,
        }

    grounding = validate_grounding(grounded_answer, retrieval["chunks"])

    if not grounding["is_valid"]:
        return {
            "question": req.question,
            "answer": "I detected an ungrounded answer, so I am not showing it as transcript-based.",
            "validation": {
                "retrieval": public_retrieval,
                "grounding": grounding,
            },
            "token_usage": usage,
        }

    return {
        "question": req.question,
        "answer": grounded_answer.answer,
        "citations": grounded_answer.citations,
        "validation": {
            "retrieval": public_retrieval,
            "grounding": grounding,
        },
        "token_usage": usage,
    }
