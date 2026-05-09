from langchain_experimental.text_splitter import SemanticChunker

from app.embeddings import get_embedding_model
from app.config import WINDOW_SIZE


def create_transcript_windows(transcript):

    windows = []
    current = []

    for i, segment in enumerate(transcript):

        current.append(segment["text"])

        if (i + 1) % WINDOW_SIZE == 0:
            windows.append(" ".join(current))
            current = []

    if current:
        windows.append(" ".join(current))

    return windows


def semantic_chunk_transcript(transcript):

    embeddings = get_embedding_model()

    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=60
    )

    windows = create_transcript_windows(transcript)

    documents = []

    for window in windows:
        docs = splitter.create_documents([window])
        documents.extend(docs)

    print(f"Created {len(documents)} semantic chunks")

    return documents
