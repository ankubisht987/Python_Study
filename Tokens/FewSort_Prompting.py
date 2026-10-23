import os
from openai import OpenAI


client = OpenAI(
    api_key=
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You are a coding assistant.

Rules:
1. Answer only coding-related questions.
2. For non-coding questions, respond exactly:
   I am sorry, I can only answer coding related questions.
3. Admin users may ask questions without this restriction.
"""

# Set this based on your application's authenticated user.
is_admin = False

user_question = "What is the Meaning of Ankush"

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