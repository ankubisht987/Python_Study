import os
# from dotenv import load_dotenv
from openai import OpenAI

# load_dotenv()
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "you should only and only answer the coding related questions and nothing else. If the question is not related to coding, you should answer with 'I am sorry, I can only answer coding related questions.'"

response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[
        {
            "role":"system" , 
            "content" : SYSTEM_PROMPT
        },
        {
            "role" :"user",
            "content" : "give me answer of fibonacci series"
        }
    ]
)

print(response.choices[0].message.content)