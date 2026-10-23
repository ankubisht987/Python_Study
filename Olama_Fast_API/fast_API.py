from fastapi import FastAPI , HTTPException
import os
from openai import OpenAI

app = FastAPI()

# 🔐 Initialize the Gemini client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
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

# 👑 Admin placeholder
is_admin = False
# 💬 Get the user's question
@app.get("/")
def user_Ques(user_question: str):

    if not user_question.strip():
        raise HTTPException(
            status_code=400,
            detail="⚠️ Please enter the question."
        )

    # 📩 Prepare messages
    if is_admin:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are CodeMate, a helpful AI assistant. "
                    "The authenticated admin may ask about any topic."
                )
            },
            {"role": "user", "content": user_question}
        ]
    else:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_question}
        ]

    # 🚀 Generate the response
    try:
        response = client.chat.completions.create(
            model="gemini-3.8-flash",
            messages=messages
        )
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Could not get a response from Gemini. Check your API key, model name, and API availability."
        )

    # ✅ Get the answer
    ans = response.choices[0].message.content

    return {
        "question": user_question,
        "answer": ans
    }