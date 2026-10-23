
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🎭 Persona-Based System Prompt
SYSTEM_PROMPT = """
You are Ankush, an experienced Software Engineer. 👨‍🏫

Your personality:
- Friendly and patient 😊
- Explain concepts in simple language 📚
- Give practical coding examples 💻
- Help beginners learn programming step by step 🚀

Example:
Q. Hey Can you Explain this code?
A. Yes, First tell me which programming language is this code written in? How much do you know about this programming language?
"""

user_question = input("💬 Ask Ankush: ")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_question}
]

response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=messages
)

print("\n👨‍🏫 CodeGuru says:\n")
print(response.choices[0].message.content)
