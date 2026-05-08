from openai import OpenAI

from app.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL
)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL
)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b:free",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)
