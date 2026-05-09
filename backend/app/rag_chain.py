from openai import OpenAI
from app.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL
from app.prompts import build_prompt


client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY
)


def get_answer(question, docs):

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = build_prompt(context, question)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
