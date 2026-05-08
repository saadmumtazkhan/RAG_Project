from openai import OpenAI
from app.config import GROK_API_KEY, GROK_BASE_URL

client = OpenAI(
    api_key=GROK_API_KEY,
    base_url=GROK_BASE_URL
)

response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)
