from app.transcript_loader import (
    fetch_transcript,
    transcript_to_text
)

from app.chunking import semantic_chunk_transcript

from app.vector_store import store_documents


def run_ingestion_pipeline():

    print("Starting transcript ingestion...")

    transcript = fetch_transcript()

    full_text = transcript_to_text(transcript)

    documents = semantic_chunk_transcript(transcript)

    store_documents(documents)

    print("Ingestion completed successfully")


if __name__ == "__main__":
    run_ingestion_pipeline()
