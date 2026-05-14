from openai import OpenAI
from app.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, LLM_MODEL
from app.prompts import build_prompt
from app.validation import token_usage_to_dict


client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY
)


def get_answer(question, context):
    prompt = build_prompt(context, question)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        # JSON output gives the validation layer a deterministic structure for
        # checking citations instead of trusting free-form model text.
        response_format={"type": "json_object"}
    )

    return {
        "content": response.choices[0].message.content,
        "usage": token_usage_to_dict(response.usage),
    }
