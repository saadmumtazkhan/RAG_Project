from langchain_community.vectorstores import Chroma

from app.embeddings import get_embedding_model

from app.config import VECTOR_DB_DIR


def store_documents(documents):

    embeddings = get_embedding_model()

    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    print("Documents stored in ChromaDB")
