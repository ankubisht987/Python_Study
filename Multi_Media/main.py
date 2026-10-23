from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    # api_key = os.getenv("OPENROUTER_API_KEY"),
    # base_url='https://openrouter.ai/api/v1'
)
print("response")
response = client.chat.completions.create(
    model="gemini-3.8-flash",
    # # model='openrouter/free',
    # model='nvidia/nemotron-3.5-super-vl:free',
    messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is inside the image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg"
                            }
                        }
                    ]
                }
            ]
)
print("response next")
print(response.choices[0].message.content)