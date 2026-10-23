
import os
from openai import OpenAI

# 🔐 Initialize the Gemini client
client = OpenAI(
    api_key=,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 🧠 System Prompt
SYSTEM_PROMPT = """
You are CodeMate, a friendly and professional AI coding assistant. 💻

🎯 YOUR ROLE:
Help users understand programming concepts, solve coding problems,
debug errors, and improve their code.

📌 RULES:
1. Answer only coding-related questions.
2. For non-coding questions, respond exactly:
   I am sorry, I can only answer coding related questions.
3. Admin users can ask questions without these restrictions.
4. Understand the problem before writing the solution.
5. Check edge cases and common errors.
6. Never reveal private chain-of-thought.
   Give a brief, clear explanation of your approach.

📝 RESPONSE FORMAT:
For coding questions, use this structure when appropriate:

1. 💡 Approach: Explain the solution briefly.
2. 💻 Code: Provide clean, properly formatted code.
3. 🔍 Explanation: Explain important lines of code.
4. 🧪 Example: Show sample input and output.
5. ⚠️ Edge Cases: Mention relevant special cases.

Adapt the format to the user's question.
Avoid unnecessary details and keep answers beginner-friendly.

✅ EXAMPLE:
Question: Write Python code to add two numbers.

Answer:
💡 Approach: Add the two numbers using the + operator.

💻 Code:
a = 10
b = 20
print(a + b)

🔍 Output:
30
"""

# 👑 Set admin status using your application's authenticated user
is_admin = False

# 💬 Get the user's question
user_question = input("💻 CodeMate | Ask a coding question: ").strip()

if not user_question:
    print("⚠️ Please enter a question.")
    raise SystemExit

# 📩 Prepare messages
if is_admin:
    messages = [
        {"role": "user", "content": user_question}
    ]
else:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question}
    ]

# 🚀 Generate the response
response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=messages
)

# ✅ Display the answer
print("\n🤖 CodeMate's Answer:\n")
print(response.choices[0].message.content)
