
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("XAI_API_KEY not found in .env file")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

try:
    response = client.chat.completions.create(
        model="grok-3-mini",
        messages=[
            {"role": "user", "content": "Say hello in one sentence."}
        ],
        max_tokens=50,
    )

    print("Grok API key is working!")
    print(response.choices[0].message.content)

except Exception as e:
    print("API request failed:", e)
