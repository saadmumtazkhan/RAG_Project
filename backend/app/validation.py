from pydantic import BaseModel, Field, ValidationError

from app.config import MIN_CONTEXT_CHARACTERS, MIN_RETRIEVAL_SCORE


class GroundedAnswer(BaseModel):
    answer: str = Field(min_length=1)
    citations: list[str]
    is_answerable: bool


def validate_retrieval(docs_with_scores):
    accepted = [
        (doc, score)
        for doc, score in docs_with_scores
        if score >= MIN_RETRIEVAL_SCORE
    ]

    context_characters = sum(
        len(doc.page_content.strip())
        for doc, _score in accepted
    )

    if not accepted:
        return {
            "is_valid": False,
            "reason": "No transcript chunks passed the relevance threshold.",
            "chunks": [],
            "scores": [],
        }

    if context_characters < MIN_CONTEXT_CHARACTERS:
        return {
            "is_valid": False,
            "reason": "Retrieved transcript context is too small to answer safely.",
            "chunks": [],
            "scores": [score for _doc, score in accepted],
        }

    # Stable per-request IDs let us verify that the model cites only chunks it saw.
    chunks = [
        {
            "id": f"chunk_{index + 1}",
            "doc": doc,
            "score": score,
        }
        for index, (doc, score) in enumerate(accepted)
    ]

    return {
        "is_valid": True,
        "reason": None,
        "chunks": chunks,
        "scores": [score for _doc, score in accepted],
    }


def public_retrieval_validation(retrieval):
    # Document objects are kept internal because they are not JSON serializable
    # and may include more transcript text than the API response needs.
    return {
        "is_valid": retrieval["is_valid"],
        "reason": retrieval["reason"],
        "scores": retrieval["scores"],
        "chunks": [
            {
                "id": chunk["id"],
                "score": chunk["score"],
            }
            for chunk in retrieval["chunks"]
        ],
    }


def build_context_from_chunks(chunks):
    return "\n\n".join(
        f"[{chunk['id']}]\n{chunk['doc'].page_content}"
        for chunk in chunks
    )


def parse_grounded_answer(raw_answer):
    try:
        return GroundedAnswer.model_validate_json(raw_answer), None
    except ValidationError:
        # A non-JSON response cannot be checked for citations, so it is treated
        # as invalid instead of being displayed as a grounded transcript answer.
        return None, "The model response was not valid grounded-answer JSON."


def validate_grounding(answer, chunks):
    allowed_citations = {chunk["id"] for chunk in chunks}
    provided_citations = set(answer.citations)

    if not answer.is_answerable:
        return {
            "is_valid": True,
            "reason": None,
        }

    if not provided_citations:
        return {
            "is_valid": False,
            "reason": "The answer was marked answerable but did not cite any retrieved chunks.",
        }

    invalid_citations = provided_citations - allowed_citations

    if invalid_citations:
        return {
            "is_valid": False,
            "reason": f"The answer cited chunks that were not retrieved: {sorted(invalid_citations)}.",
        }

    return {
        "is_valid": True,
        "reason": None,
    }


def token_usage_to_dict(usage):
    if usage is None:
        return None

    return {
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
    }
