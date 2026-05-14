from langchain_community.vectorstores import Chroma
from app.embeddings import get_embedding_model
from app.config import RETRIEVAL_K, VECTOR_DB_DIR


def load_vectorstore():

    embeddings = get_embedding_model()

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings
    )

    return vectorstore


def retrieve_docs(query, k=RETRIEVAL_K):

    vectorstore = load_vectorstore()

    # Scores let the API validate whether the retrieved chunks are strong enough
    # before spending tokens on an answer that may not be grounded.
    docs_with_scores = vectorstore.similarity_search_with_relevance_scores(
        query,
        k=k
    )

    return docs_with_scores
