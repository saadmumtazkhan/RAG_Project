def build_prompt(context, question):

    return f"""
You are a helpful assistant.
Answer ONLY using the context below.

If the answer is not in the context, say "I don't know".

---

Context:
{context}

---

Question:
{question}

---

Answer:
"""
