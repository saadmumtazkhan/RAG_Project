from langchain_community.vectorstores import Chroma
from app.embeddings import get_embedding_model
from app.config import VECTOR_DB_DIR


def load_vectorstore():

    embeddings = get_embedding_model()

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=embeddings
    )

    return vectorstore


def retrieve_docs(query, k=5):

    vectorstore = load_vectorstore()

    docs = vectorstore.similarity_search(
        query,
        k=k
    )

    return docs
