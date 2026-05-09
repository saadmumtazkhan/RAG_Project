from app.retriever import retrieve_docs
from app.rag_chain import get_answer


def ask(question):

    docs = retrieve_docs(question)

    answer = get_answer(question, docs)

    return answer


if __name__ == "__main__":

    while True:

        q = input("\nAsk: ")

        if q.lower() in ["exit", "quit"]:
            break

        response = ask(q)

        print("\nAnswer:\n", response)
