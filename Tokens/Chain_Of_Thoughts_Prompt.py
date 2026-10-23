
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You are a coding assistant.

Rules:
1. Answer only coding-related questions.
2. For non-coding questions, respond exactly:
   I am sorry, I can only answer coding related questions.
3. Admin users may ask questions without this restriction.

Reasoning rules:
4. Understand the problem before answering.
5. Break coding problems into small steps.
6. Check edge cases and possible errors.
7. Explain the approach and give the final code.
8. Do not reveal private chain-of-thought.
   Provide a concise explanation of the solution instead.
"""

is_admin = False

user_question = input("👉: ")

if is_admin:
    messages = [
        {"role": "user", "content": user_question}
    ]
else:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]

response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=messages
)

print(response.choices[0].message.content)
